from django.urls import path

from .views import AlertCreateView, AlertListView

urlpatterns = [
    path('', AlertCreateView.as_view(), name='create-alert'),
    path('my/', AlertListView.as_view(), name='list-alerts'),
]
