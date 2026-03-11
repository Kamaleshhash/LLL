from rest_framework import serializers

from .models import CaseEvent, CaseRecord, LandParcel, ParcelCaseLink


class CaseEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CaseEvent
        fields = ['event_date', 'title', 'description']


class CaseRecordSerializer(serializers.ModelSerializer):
    events = CaseEventSerializer(many=True, read_only=True)

    class Meta:
        model = CaseRecord
        fields = [
            'cnr_number',
            'case_type',
            'court_name',
            'petitioner',
            'respondent',
            'filing_date',
            'last_hearing_date',
            'next_hearing_date',
            'status',
            'stage',
            'order_pdf_url',
            'summary',
            'risk_score',
            'events',
        ]


class LandParcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandParcel
        fields = [
            'id',
            'state',
            'district',
            'taluk',
            'village_name',
            'survey_number',
            'owner_name',
            'area_hectare',
            'land_type',
            'geojson_boundary',
            'ror_reference',
            'verification_hash',
        ]


class ParcelCaseLinkSerializer(serializers.ModelSerializer):
    case = CaseRecordSerializer(read_only=True)

    class Meta:
        model = ParcelCaseLink
        fields = ['case', 'relevance_score', 'is_primary']
