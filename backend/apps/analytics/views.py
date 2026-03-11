from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.records.models import ParcelCaseLink


class HotspotAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hotspots = (
            ParcelCaseLink.objects.values('parcel__state', 'parcel__district', 'parcel__village_name')
            .annotate(case_count=Count('case_id'))
            .order_by('-case_count')[:20]
        )
        return Response({'hotspots': list(hotspots)})
