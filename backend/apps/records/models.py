from django.db import models


class LandParcel(models.Model):
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    taluk = models.CharField(max_length=100, blank=True)
    village_name = models.CharField(max_length=150)
    survey_number = models.CharField(max_length=50)
    owner_name = models.CharField(max_length=255)
    area_hectare = models.DecimalField(max_digits=8, decimal_places=2)
    land_type = models.CharField(max_length=120)
    geojson_boundary = models.JSONField(default=dict, blank=True)
    ror_reference = models.CharField(max_length=200, blank=True)
    verification_hash = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('state', 'district', 'village_name', 'survey_number', 'owner_name')


class CaseRecord(models.Model):
    CASE_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('disposed', 'Disposed'),
        ('stayed', 'Stayed'),
    ]

    cnr_number = models.CharField(max_length=32, unique=True)
    case_type = models.CharField(max_length=120)
    court_name = models.CharField(max_length=255)
    petitioner = models.CharField(max_length=255)
    respondent = models.CharField(max_length=255)
    filing_date = models.DateField(null=True, blank=True)
    last_hearing_date = models.DateField(null=True, blank=True)
    next_hearing_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=CASE_STATUS_CHOICES)
    stage = models.CharField(max_length=255, blank=True)
    order_pdf_url = models.URLField(blank=True)
    summary = models.TextField(blank=True)
    risk_score = models.FloatField(default=0.0)


class ParcelCaseLink(models.Model):
    parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='case_links')
    case = models.ForeignKey(CaseRecord, on_delete=models.CASCADE, related_name='parcel_links')
    relevance_score = models.FloatField(default=1.0)
    is_primary = models.BooleanField(default=False)

    class Meta:
        unique_together = ('parcel', 'case')


class CaseEvent(models.Model):
    case = models.ForeignKey(CaseRecord, on_delete=models.CASCADE, related_name='events')
    event_date = models.DateField()
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['-event_date']


class VerificationLog(models.Model):
    source_system = models.CharField(max_length=120)
    source_reference = models.CharField(max_length=200)
    payload_hash = models.CharField(max_length=64)
    signature = models.CharField(max_length=255, blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)
