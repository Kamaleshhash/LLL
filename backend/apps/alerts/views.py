from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AlertSubscription
from .serializers import AlertSubscriptionSerializer


class AlertCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AlertSubscriptionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({'message': 'Alert created', 'alert': serializer.data})


class AlertListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        alerts = AlertSubscription.objects.filter(user=request.user).order_by('-created_at')
        return Response(AlertSubscriptionSerializer(alerts, many=True).data)
