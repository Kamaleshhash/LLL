from django.db.models import Count, Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from landlitigation.permissions import IsAdminOrOfficial
from apps.records.models import CaseRecord
from apps.records.serializers import CaseRecordSerializer, LandParcelSerializer, ParcelCaseLinkSerializer

from .models import BulkSearchJob, SearchLog
from .serializers import BulkSearchSerializer, NLQSerializer, SearchRequestSerializer
from .services import autocomplete_village, filter_case_links, load_mock_data, search_parcels, semantic_search


class HealthCheckView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({'status': 'ok', 'service': 'land-litigation-api'})


class SearchView(APIView):
    def post(self, request):
        serializer = SearchRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        load_mock_data()

        parcels, ranking = search_parcels(
            state=data['state'],
            district=data['district'],
            village_name=data['village_name'],
            survey_number=data['survey_number'],
        )

        results = []
        for parcel in parcels:
            links = filter_case_links(
                parcel,
                case_type=data.get('case_type', ''),
                status=data.get('status', ''),
                from_date=data.get('from_date'),
                to_date=data.get('to_date'),
            )
            results.append(
                {
                    'parcel': LandParcelSerializer(parcel).data,
                    'cases': ParcelCaseLinkSerializer(links, many=True).data,
                    'verification': {
                        'badge': 'Verified',
                        'hash': parcel.verification_hash,
                        'method': 'SHA-256 + source log',
                    },
                }
            )

        SearchLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            state=data['state'],
            district=data['district'],
            village_name=data['village_name'],
            survey_number=data['survey_number'],
            filters={
                'case_type': data.get('case_type', ''),
                'status': data.get('status', ''),
            },
            result_count=len(results),
        )

        if not results:
            return Response(
                {
                    'results': [],
                    'manual_verification_tips': [
                        'Try alternate village spelling.',
                        'Check taluk-level RoR office records for non-digitized entries.',
                        'Verify with court CNR directly at eCourts.',
                    ],
                    'fallback_message': 'No direct digital match found. Data may be partially digitized.',
                }
            )

        return Response({'results': results, 'ranking_debug': ranking})


class CaseDetailView(APIView):
    def get(self, request, cnr_number):
        case = CaseRecord.objects.filter(cnr_number=cnr_number).first()
        if not case:
            return Response({'detail': 'Case not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CaseRecordSerializer(case).data)


class VillageAutocompleteView(APIView):
    def get(self, request):
        state = request.query_params.get('state', '')
        district = request.query_params.get('district', '')
        query = request.query_params.get('query', '')
        data = autocomplete_village(state, district, query)
        return Response({'suggestions': data})


class NLPQueryView(APIView):
    def post(self, request):
        serializer = NLQSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cases = semantic_search(serializer.validated_data['query'])
        return Response({'cases': CaseRecordSerializer(cases, many=True).data})


class BulkSearchView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrOfficial]

    def post(self, request):
        serializer = BulkSearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        items = serializer.validated_data['items']
        output = []
        for item in items:
            parcels, _ = search_parcels(
                state=item.get('state', ''),
                district=item.get('district', ''),
                village_name=item.get('village_name', ''),
                survey_number=item.get('survey_number', ''),
            )
            output.append(
                {
                    'query': item,
                    'matches': parcels.count(),
                    'pending_cases': parcels.aggregate(
                        pending=Count('case_links__case', filter=Q(case_links__case__status='pending'))
                    ).get('pending', 0),
                }
            )

        job = BulkSearchJob.objects.create(requested_by=request.user, payload={'items': items}, output={'rows': output}, status='completed')
        return Response({'job_id': job.id, 'output': output})
