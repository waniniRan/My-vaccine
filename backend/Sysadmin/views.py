from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.core.paginator import Paginator
#from rest_framework.renderers import TemplateHTMLRenderer
from django.contrib.admin.models import LogEntry
import csv
import logging
from openpyxl import Workbook
from django.http import HttpResponse
import logging
from api.serializers import (HealthFacilitySerializer, VaccineSerializer,FacilityAdminCreationSerializer, UserSerializer)
from .models import User,HealthFacility,Vaccine,FacilityAdmin
from django.views import View
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.decorators import action
from rest_framework import viewsets



logger = logging.getLogger(__name__)


#SYSTEM ADMIN 
class IsSystemAdmin(permissions.BasePermission):
    #System admin to only allow system admins to access views.

    def has_permission(self, request, view):
        return (
        request.user and
        request.user.is_authenticated and
        hasattr (request.user, 'role') and
        request.user.role == 'SYSTEM_ADMIN'
        )
#END

#FACILITY ADMIN
class IsFacilityAdmin(permissions.BasePermission):
   #facility admins to access views.

    def has_permission(self, request, view):
        return (
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'role') and 
            request.user.role == 'FACILITY_ADMIN'
        )
#END

# Authentication Views
class LoginAPIView(APIView):
    
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.id,
                    'username': user.username,
                    'role': user.role,
                    'must_change_password': getattr(user, 'must_change_password', False)
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Account is disabled'
                }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Delete the user's token
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({
                'message': 'Successfully logged out'
            }, status=status.HTTP_200_OK)

# Dashboard Views
class SystemAdminDashboardAPIView(APIView):
    """
    System Admin Dashboard API
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]
    
    def get(self, request):
        try:
            dashboard_data = {
                'message': 'Welcome System Administrator',
                'stats': {
                    'facility_count': HealthFacility.objects.count(),
                    'vaccine_count': Vaccine.objects.count(),
                    'facility_admin_count': User.objects.filter(role='FACILITY_ADMIN').count(),
                    'active_facilities': HealthFacility.objects.filter(is_active=True).count(),
                    'active_vaccines': Vaccine.objects.filter(is_active=True).count(),
                },
                'recent_facilities': HealthFacilitySerializer(
                    HealthFacility.objects.order_by('-created_at')[:5], 
                    many=True
                ).data,
                'recent_vaccines': VaccineSerializer(
                    Vaccine.objects.order_by('-created_at')[:5], 
                    many=True
                ).data
            }
            return Response(dashboard_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Dashboard error: {str(e)}")
            return Response({
                'error': 'Failed to load dashboard data'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#END

# Health Facility API Views
class HealthFacilityListCreateAPIView(generics.ListCreateAPIView):
    queryset = HealthFacility.objects.all()
    serializer_class = HealthFacilitySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]
    
    def get_queryset(self):
        queryset = HealthFacility.objects.select_related('admin', 'created_by').order_by('-created_at')
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                location__icontains=search
            )
        
        # Filter by type
        facility_type = self.request.query_params.get('type', None)
        if facility_type:
            queryset = queryset.filter(facility_type=facility_type)
        
        # Filter by status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save(created_by=self.request.user)
        except Exception as e:
            logger.error(f"Error creating facility: {str(e)}")
            raise
#END


class HealthFacilityDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HealthFacility.objects.all()
    serializer_class = HealthFacilitySerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]
    
    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except Exception as e:
            logger.error(f"Error updating facility: {str(e)}")
            raise
#END

#CREATE FACILITY ADMIN
class CreateFacilityWithAdminAPIView(APIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]

    def post(self, request):
        serializer = FacilityAdminCreationSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    # Create Facility Admin user
                    admin_user = User.objects.create_user(
                        username=serializer.validated_data['admin_username'],
                        email=serializer.validated_data['admin_email'],
                        password=serializer.validated_data['admin_password'],
                        role='FACILITY_ADMIN',
                        must_change_password=True
                    )

                    # Create Health Facility
                    facility = HealthFacility.objects.create(
                        name=serializer.validated_data['facility_name'],
                        facility_type=serializer.validated_data['facility_type'],
                        location=serializer.validated_data.get('facility_location', ''),
                        phone=serializer.validated_data.get('facility_phone', ''),
                        email=serializer.validated_data.get('facility_email', ''),
                        admin=admin_user,
                        created_by=request.user
                    )

                    # Return facility data with admin info
                    facility_serializer = HealthFacilitySerializer(facility)
                    return Response({
                        'message': 'Facility and admin created successfully',
                        'facility': facility_serializer.data
                    }, status=status.HTTP_201_CREATED)
                    
            except Exception as e:
                logger.error(f"Error creating facility with admin: {str(e)}")
                return Response({
                    'error': 'Failed to create facility and admin user'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#END

# Vaccine API Views
class VaccineListCreateAPIView(generics.ListCreateAPIView):
    """
    List all vaccines or create a new vaccine
    """
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]
    
    def get_queryset(self):
        queryset = Vaccine.objects.prefetch_related('facility').order_by('-created_at')
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                name__icontains=search
            ) | queryset.filter(
                diseasePrevented__icontains=search
            )
        
        # Filter by facility
        facility_id = self.request.query_params.get('facility', None)
        if facility_id:
            queryset = queryset.filter(facility__id=facility_id)
        
        # Filter by status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                serializer.save(created_by=self.request.user)
        except Exception as e:
            logger.error(f"Error creating vaccine: {str(e)}")
            raise
#END

#VACCINE DETAILS
class VaccineDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a vaccine
    """
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]
    
    def perform_update(self, serializer):
        try:
            with transaction.atomic():
                serializer.save()
        except Exception as e:
            logger.error(f"Error updating vaccine: {str(e)}")
            raise
#END

# Status Toggle Views
class ToggleFacilityStatusAPIView(APIView):
    """
    Toggle facility active/inactive status
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]
    
    def post(self, request, facility_id):
        try:
            facility = get_object_or_404(HealthFacility, id=facility_id)
            facility.is_active = not facility.is_active
            facility.save()
            
            return Response({
                'success': True,
                'is_active': facility.is_active,
                'message': f'Facility {"activated" if facility.is_active else "deactivated"} successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error toggling facility status: {str(e)}")
            return Response({
                'success': False,
                'message': 'An error occurred while updating the facility status'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#END        

class ToggleVaccineStatusAPIView(APIView):
    """
    Toggle vaccine active/inactive status
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]
    
    def post(self, request, vaccine_id):
        try:
            vaccine = get_object_or_404(Vaccine, id=vaccine_id)
            vaccine.is_active = not vaccine.is_active
            vaccine.save()
            
            return Response({
                'success': True,
                'is_active': vaccine.is_active,
                'message': f'Vaccine {"activated" if vaccine.is_active else "deactivated"} successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error toggling vaccine status: {str(e)}")
            return Response({
                'success': False,
                'message': 'An error occurred while updating the vaccine status'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#END        

# List 
class FacilityAdminListAPIView(generics.ListAPIView):
    """
    List all facility admins
    """
    queryset = User.objects.filter(role='FACILITY_ADMIN').select_related('managed_facility')
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]

#END    

#FACILITY DETAILS
class FacilityAdminDetailAPIView(generics.RetrieveAPIView):
    """
    Retrieve facility admin details
    """
    queryset = User.objects.filter(role='FACILITY_ADMIN').select_related('managed_facility')
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]
#END

# Report Generation Views
class GenerateReportAPIView(APIView):
    """
    Generate various system reports
    """
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsSystemAdmin]
    
    def post(self, request):
        report_type = request.data.get('report_type')
        format_type = request.data.get('format', 'json')
        filters = request.data.get('filters', {})
        
        # Validate report type
        if not report_type:
            return Response({
                'error': 'Report type is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if report_type == 'facilities':
                return self._generate_facilities_report(format_type, filters)
            elif report_type == 'vaccines':
                return self._generate_vaccines_report(format_type, filters)
            elif report_type == 'users':
                return self._generate_users_report(format_type, filters)
            else:
                return Response({
                    'error': 'Invalid report type'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error generating report: {str(e)}")
            return Response({
                'error': 'Failed to generate report'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _generate_facilities_report(self, format_type, filters):
        queryset = HealthFacility.objects.select_related('admin', 'created_by')
        
        if filters.get('is_active') is not None:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if format_type == 'json':
            serializer = HealthFacilitySerializer(queryset, many=True)
            return Response({
                'report_type': 'facilities',
                'data': serializer.data,
                'count': queryset.count()
            })
        elif format_type == 'csv':
            return self._export_facilities_csv(queryset)
        
    def _generate_vaccines_report(self, format_type, filters):
        queryset = Vaccine.objects.prefetch_related('facility')
        
        if filters.get('is_active') is not None:
            queryset = queryset.filter(is_active=filters['is_active'])
        
        if format_type == 'json':
            serializer = VaccineSerializer(queryset, many=True)
            return Response({
                'report_type': 'vaccines',
                'data': serializer.data,
                'count': queryset.count()
            })
        elif format_type == 'csv':
            return self._export_vaccines_csv(queryset)
    
    def _export_facilities_csv(self, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="facilities_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Type', 'Location', 'Admin', 'Active', 'Created At'])
        
        for facility in queryset:
            writer.writerow([
                facility.name,
                facility.get_facility_type_display(),
                facility.location,
                facility.admin.username if facility.admin else 'No Admin',
                'Yes' if facility.is_active else 'No',
                facility.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
    
    def _export_vaccines_csv(self, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="vaccines_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Name', 'Disease Prevented', 'Facilities', 'Active', 'Created At'])
        
        for vaccine in queryset:
            facilities = ', '.join([f.name for f in vaccine.facility.all()])
            writer.writerow([
                vaccine.name,
                vaccine.diseasePrevented,
                facilities,
                'Yes' if vaccine.is_active else 'No',
                vaccine.created_at.strftime('%Y-%m-%d %H:%M')
            ])
        
        return response
    #END
#END

class FacilityAdminViewSet(viewsets.ModelViewSet):

    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Reset worker's password"""
        worker = get_object_or_404(FacilityAdmin, pk=pk)
        
        # Generate new temporary password (you might want to use a more secure method)
        import secrets
        import string
        
        alphabet = string.ascii_letters + string.digits
        new_password = ''.join(secrets.choice(alphabet) for i in range(12))
        
        worker.temporary_password = new_password
        worker.password_changed = False
        worker.save()
        
        return Response({
            'message': f'Password reset for {worker.get_full_name()}.',
            'temporary_password': new_password
        })


class DashboardAPIView(APIView):
    def get(self, request):
        # Your dashboard logic here
        data = {
            'message': 'Dashboard data',
            # Add your dashboard data
        }
        return Response(data, status=status.HTTP_200_OK)
