from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import update_last_login
from HealthcareW.models.Guardian import Guardian
from Sysadmin.models.User import User
from rest_framework.permissions import IsAuthenticated

class HealthcareWorkerLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and hasattr(user, 'healthcareworker'):
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': 'healthcareworker',
                'user_id': user.id,
                'username': user.username
            })
        return Response({'detail': 'Invalid credentials or not a healthcare worker.'}, status=status.HTTP_401_UNAUTHORIZED)

class GuardianLoginView(APIView):
    def post(self, request):
        national_id = request.data.get('national_id')
        password = request.data.get('password')
        try:
            guardian = Guardian.objects.get(national_id=national_id)
            user = guardian.user
        except Guardian.DoesNotExist:
            return Response({'detail': 'Guardian not found.'}, status=status.HTTP_404_NOT_FOUND)
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': 'guardian',
                'user_id': user.id,
                'national_id': guardian.national_id,
                'password_changed': guardian.password_changed
            })
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

class HealthcareWorkerChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password changed successfully.'})

class GuardianChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        try:
            guardian = Guardian.objects.get(user=user)
        except Guardian.DoesNotExist:
            return Response({'detail': 'Guardian not found.'}, status=status.HTTP_404_NOT_FOUND)
        if not user.check_password(old_password):
            return Response({'detail': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_password)
        user.save()
        guardian.password_changed = True
        guardian.save()
        return Response({'detail': 'Password changed successfully.'}) 