from django.urls import path

from .views import HotspotAnalyticsView

urlpatterns = [
    path('hotspots/', HotspotAnalyticsView.as_view(), name='hotspot-analytics'),
]
