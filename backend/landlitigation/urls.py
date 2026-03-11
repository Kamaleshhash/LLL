from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.search_api.views import HealthCheckView

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', HealthCheckView.as_view(), name='health-check'),
    path('api/auth/', include('apps.accounts.urls')),
    path('api/search/', include('apps.search_api.urls')),
    path('api/alerts/', include('apps.alerts.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
    path('api/reports/', include('apps.reports.urls')),
]
