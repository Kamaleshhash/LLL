import random
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OTPRequest
from .serializers import OTPRequestSerializer, OTPVerifySerializer, UserSerializer

User = get_user_model()


class OTPRequestView(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = f"{random.randint(100000, 999999)}"
        OTPRequest.objects.create(email=email, otp=otp)
        return Response(
            {
                'message': 'OTP generated (mock mode)',
                'debug_otp': otp,
                'expires_in_minutes': settings.OTP_EXPIRY_MINUTES,
            }
        )


class OTPVerifyView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        otp = serializer.validated_data['otp']

        cutoff = timezone.now() - timedelta(minutes=settings.OTP_EXPIRY_MINUTES)
        otp_request = OTPRequest.objects.filter(
            email=email, otp=otp, is_used=False, created_at__gte=cutoff
        ).order_by('-created_at').first()

        if not otp_request:
            return Response({'detail': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={'username': email.split('@')[0], 'role': request.data.get('role', 'individual')},
        )
        otp_request.is_used = True
        otp_request.save(update_fields=['is_used'])

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
