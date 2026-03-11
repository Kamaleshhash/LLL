from django.urls import path

from .views import (
    BulkSearchView,
    CaseDetailView,
    NLPQueryView,
    SearchView,
    VillageAutocompleteView,
)

urlpatterns = [
    path('', SearchView.as_view(), name='parcel-search'),
    path('cases/<str:cnr_number>/', CaseDetailView.as_view(), name='case-detail'),
    path('autocomplete/village/', VillageAutocompleteView.as_view(), name='village-autocomplete'),
    path('nlq/', NLPQueryView.as_view(), name='nlq-search'),
    path('bulk/', BulkSearchView.as_view(), name='bulk-search'),
]
