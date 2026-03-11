from django.urls import path

from .views import CaseSummaryPDFView

urlpatterns = [
    path('case-summary/<str:cnr_number>/', CaseSummaryPDFView.as_view(), name='case-summary-pdf'),
]
