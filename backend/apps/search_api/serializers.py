from rest_framework import serializers


class SearchRequestSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=100)
    district = serializers.CharField(max_length=100)
    village_name = serializers.CharField(max_length=150)
    survey_number = serializers.CharField(max_length=50)
    case_type = serializers.CharField(max_length=120, required=False, allow_blank=True)
    status = serializers.CharField(max_length=20, required=False, allow_blank=True)
    from_date = serializers.DateField(required=False)
    to_date = serializers.DateField(required=False)


class NLQSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=300)


class BulkSearchSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False,
        max_length=200,
    )
