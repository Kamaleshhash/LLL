from django.contrib import admin

from .models import CaseEvent, CaseRecord, LandParcel, ParcelCaseLink, VerificationLog

admin.site.register(LandParcel)
admin.site.register(CaseRecord)
admin.site.register(ParcelCaseLink)
admin.site.register(CaseEvent)
admin.site.register(VerificationLog)
