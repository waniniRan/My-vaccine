from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from Sysadmin.models.FacilityAdmin import FacilityAdmin
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([AllowAny])
def facility_admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    
    try:
        fa = FacilityAdmin.objects.get(admin_username=username)
    except FacilityAdmin.DoesNotExist:
        return Response({"detail": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
    
    # first check temporary password
    if fa.password_changed == False and password == fa.temporary_password:
        user = fa.user
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "password_change_required": True
        })
    
    # check normal user password (Django User table)
    user = authenticate(username=username, password=password)
    if user is not None and user.facility_admin.is_active:
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "password_change_required": False
        })
    else:
        return Response({"detail": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def facility_admin_change_password(request):
    user = request.user
    new_password = request.data.get("new_password")

    if not new_password:
        return Response({"detail": "New password required"}, status=400)

    user.set_password(new_password)
    user.save()

    fa = user.facility_admin
    fa.password_changed = True
    fa.save()

    return Response({"detail": "Password changed successfully"})

