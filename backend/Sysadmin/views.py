from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User, SystemReport,HealthFacility,Vaccine
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from .permissions import IsSystemAdmin
from django.core.paginator import Paginator
import csv
from django.db import transaction
from django.views.decorators.http import require_http_methods
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from io import StringIO, BytesIO
from openpyxl import Workbook
from api.serializers import (HealthFacilitySerializer, VaccineSerializer,FacilityAdminCreationSerializer)
from .forms import FacilityAdminCreationForm, Vaccinationform , healthfacilityform
import logging
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)




#SYSTEM ADMIN
class SystemAdminDashboard(APIView):
    permission_classes = [IsSystemAdmin]
    
    def get(self, request):
        return Response({
            'message': 'Welcome System Administrator',
            'actions': [
                'Manage all users',
                'Configure system settings',
                'Create facilities'
            ]
        })
#END

#Reports by System admin
class ReportBaseView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == User.Role.SYSTEM_ADMIN

class GenerateReportView(ReportBaseView, APIView):
    def post(self, request):
        report_type = request.data.get('report_type')
        format = request.data.get('format', 'csv')
        filters = request.data.get('filters', {})
        
        # Validate report type
        valid_types = dict(SystemReport.REPORT_TYPES).keys()
        if report_type not in valid_types:
            return Response({'error': 'Invalid report type'}, status=400)
        
        # Generate report based on type
        if report_type == 'USER_ACTIVITY':
            return self._generate_user_activity_report(format, filters)
        elif report_type == 'LOGIN_HISTORY':
            return self._generate_login_history_report(format, filters)
        # Add other report types here...
        
    def _generate_user_activity_report(self, format, filters):
        # Example implementation
        from django.contrib.admin.models import LogEntry
        queryset = LogEntry.objects.all()
        
        if filters.get('start_date'):
            queryset = queryset.filter(action_time__gte=filters['start_date'])
        if filters.get('end_date'):
            queryset = queryset.filter(action_time__lte=filters['end_date'])
        
        if format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="user_activity.csv"'
            
            writer = csv.writer(response)
            writer.writerow(['Timestamp', 'User', 'Action', 'Object'])
            
            for entry in queryset:
                writer.writerow([
                    entry.action_time,
                    entry.user.get_full_name(),
                    entry.get_action_flag_display(),
                    str(entry.object_repr)
                ])
            
            return response
        
        elif format == 'excel':
            output = BytesIO()
            wb = Workbook()
            ws = wb.active
            ws.title = "User Activity"
            
            # Add headers
            ws.append(['Timestamp', 'User', 'Action', 'Object'])
            
            # Add data
            for entry in queryset:
                 ws.append([
                    entry.action_time,
                    entry.user.get_full_name(),
                    entry.get_action_flag_display(),
                    str(entry.object_repr)
                 ])
            
            wb.save(output)
            response = HttpResponse(
                output.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename="user_activity.xlsx"'
            return response
        
        return Response({'error': 'Unsupported format'}, status=400)

class ReportListView(ReportBaseView, APIView):
    def get(self, request):
        reports = SystemReport.objects.filter(generated_by=request.user).order_by('-generated_at')
        data = [{
            'id': report.id,
            'report_type': report.get_report_type_display(),
            'generated_at': report.generated_at,
            'parameters': report.parameters,
            'is_downloaded': report.is_downloaded
        } for report in reports]
        return Response(data)

class DownloadReportView(ReportBaseView, View):
    def get(self, request, report_id):
        try:
            report = SystemReport.objects.get(id=report_id, generated_by=request.user)
            response = HttpResponse(report.report_file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{report.report_file.name.split("/")[-1]}"'
            
            # Mark as downloaded
            report.is_downloaded = True
            report.save()
            
            return response
        except SystemReport.DoesNotExist:
            return HttpResponse(status=404)
#END


#FACILITY ADMIN 
class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'SYSTEM_ADMIN'
    def is_system_admin(user):
     return user.role == 'SYSTEM_ADMIN'
#END

#HEALTH FACILITY & VACCINE 
class HealthFacilityListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSystemAdmin]
    queryset = HealthFacility.objects.all()
    serializer_class = HealthFacilitySerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class HealthFacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSystemAdmin]
    queryset = HealthFacility.objects.all()
    serializer_class = HealthFacilitySerializer

class CreateFacilityWithAdminView(generics.CreateAPIView):
    permission_classes = [IsSystemAdmin]
    serializer_class = FacilityAdminCreationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        #Create Facility Admin user
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
            admin=admin_user,
            created_by=request.user
        )

        #Return facility data with admin info
        facility_serializer = HealthFacilitySerializer(facility)
        return Response(facility_serializer.data, status=status.HTTP_201_CREATED)

class VaccineListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsSystemAdmin]
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class VaccineDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsSystemAdmin]
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
#END

logger = logging.getLogger(__name__)

#LOGIN VIEWS
@csrf_exempt
@login_required
@staff_member_required
def dashboard(request):
 try:
    context = {
            'facility_count': HealthFacility.objects.count(),
            'vaccine_count': Vaccine.objects.count(),  
            'admin_count': User.objects.filter(role='FACILITY_ADMIN').count(),
    
    }
    return render(request, 'sysadmin/dashboard.html', context)
 except Exception as e:
        logger.error(f"Dashboard error: {str(e)}")
        messages.error(request, "An error occurred while loading the dashboard.")
        return render(request, 'sysadmin/dashboard.html', {})

@csrf_exempt
@login_required
@staff_member_required
def facilities(request):
    """Enhanced facilities list with search and pagination"""
    facility_list = HealthFacility.objects.select_related('admin').order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        facility_list = facility_list.filter(
            name__icontains=search_query
        ) | facility_list.filter(
            location__icontains=search_query
        )
    
    # Filter by type
    facility_type = request.GET.get('type', '')
    if facility_type:
        facility_list = facility_list.filter(facility_type=facility_type)
    
    # Pagination
    paginator = Paginator(facility_list, 10)
    page_number = request.GET.get('page')
    facilities_page = paginator.get_page(page_number)
    
    context = {
        'facilities': facilities_page,
        'search_query': search_query,
        'facility_type': facility_type,
        'facility_types': HealthFacility.FACILITY_TYPES,
        'total_count': facility_list.count()
    }
    return render(request, 'sysadmin/facilities.html', context)

@csrf_exempt
@login_required
@staff_member_required
def create_facility(request):
    if request.method == 'POST':
        form = healthfacilityform(request.POST)
        if form.is_valid():
           try:
                  with transaction.atomic():
                      facility = form.save(commit=False)
                      facility.created_by = request.user
                      facility.save()
                    
                      messages.success(request, f'Successfully created facility: {facility.name}')
                    
                      return redirect('sysadmin:facilities')
           except Exception as e:
                logger.error(f"Error creating facility: {str(e)}")
                messages.error(request, "An error occurred while creating the facility.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = healthfacilityform()
    
    return render(request, 'sysadmin/create_facility.html', {'form': form})


@csrf_exempt
@login_required
@staff_member_required
def create_vaccine(request):
    if request.method == 'POST':
        form = Vaccinationform(request.POST)
        if form.is_valid():
            try:
                 with transaction.atomic():
                       vaccine = form.save(commit=False)
                       vaccine.created_by = request.user
                       vaccine.save()
            
                       # Handle ManyToMany field for facilities
                       form.save_m2m()
            
                       messages.success(request, f'Successfully created vaccine: {vaccine.name}')
                       return redirect('sysadmin:vaccines')
            except Exception as e:
                logger.error(f"Error creating vaccine: {str(e)}")
                messages.error(request, "An error occurred while creating the vaccine.")
        else : 
            messages.error(request, "Please correct the error below.")

    else:
        form = Vaccinationform()
    
    return render(request, 'sysadmin/create_vaccine.html', {'form': form})


@csrf_exempt
@login_required
@staff_member_required
def vaccines(request):
    vaccine_list = Vaccine.objects.prefetch_related('facility').order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        vaccine_list = vaccine_list.filter(
            name__icontains=search_query
        ) | vaccine_list.filter(
            diseasePrevented__icontains=search_query
        )
    
    # Filter by facility
    facility_id = request.GET.get('facility', '')
    if facility_id:
        vaccine_list = vaccine_list.filter(facility__id=facility_id)
    
    # Pagination
    paginator = Paginator(vaccine_list, 10)
    page_number = request.GET.get('page')
    vaccines_page = paginator.get_page(page_number)
    
    context = {
        'vaccines': vaccines_page,
        'search_query': search_query,
        'facility_id': facility_id,
        'facilities': HealthFacility.objects.filter(is_active=True),
        'total_count': vaccine_list.count()
    }
    return render(request, 'sysadmin/vaccines.html', context)


@csrf_exempt
@login_required
@staff_member_required
def create_facility_admin(request):
    if request.method == 'POST':
        form = FacilityAdminCreationForm(request.POST)
        if form.is_valid():
            try:
                 with transaction.atomic():
                     
                  # Create Facility Admin User
                  admin_user = User.objects.create_user(
                  username=form.cleaned_data['username'],
                  email=form.cleaned_data['email'],
                  password=form.cleaned_data['password'],
                  role='FACILITY_ADMIN',
                  must_change_password=True
                        )
            
                  # Create Health Facility
                 facility = HealthFacility.objects.create(
                 name=form.cleaned_data['facility_name'],
                 facility_type=form.cleaned_data['facility_type'],
                 location= form.cleaned_data['facility_location'],
                 phone= form.cleaned_data['facility_phone'],
                 email= form.cleaned_data['facility_email'],
                 admin=admin_user,
                 created_by=request.user
                   )
            
                 messages.success(request, f'Successfully created {facility.name} with admin {admin_user.username}')
            
                 return redirect('sysadmin:facilities')
            except Exception as e:
                logger.error(f"Error creating facility admin: {str(e)}")
                messages.error(request, "An error occurred while creating the facility and admin.")
        else:
            messages.error(request, "Please correct the errors below.")          
    else:
        form = FacilityAdminCreationForm()
    
    return render(request, 'sysadmin/create_facility_admin.html', {'form': form}) 

@csrf_exempt
@login_required
@staff_member_required
def facility_admin_detail(request, admin_id):
    admin = get_object_or_404(
        User.objects.select_related('managed_facility'),
        id=admin_id,
        role='FACILITY_ADMIN'
    )

    try:
          facility = admin.managed_facility
    except:
         facility=None

         context = {
        'admin': admin,
        'facility': facility,
        'last_login': admin.last_login.strftime('%Y-%m-%d %H:%M') if admin.last_login else 'Never'
                  }
    return render(request, 'sysadmin/facility_admin_detail.html', context)

@login_required
@staff_member_required
@require_http_methods(["POST"])
def toggle_facility_status(request, facility_id):
    """Toggle facility active/inactive status via AJAX"""
    try:
        facility = get_object_or_404(HealthFacility, id=facility_id)
        facility.is_active = not facility.is_active
        facility.save()
        
        return JsonResponse({
            'success': True,
            'is_active': facility.is_active,
            'message': f'Facility {"activated" if facility.is_active else "deactivated"} successfully'
        })
    except Exception as e:
        logger.error(f"Error toggling facility status: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while updating the facility status'
        })

@login_required
@staff_member_required
@require_http_methods(["POST"])
def toggle_vaccine_status(request, vaccine_id):
    """Toggle vaccine active/inactive status via AJAX"""
    try:
        vaccine = get_object_or_404(Vaccine, id=vaccine_id)
        vaccine.is_active = not vaccine.is_active
        vaccine.save()
        
        return JsonResponse({
            'success': True,
            'is_active': vaccine.is_active,
            'message': f'Vaccine {"activated" if vaccine.is_active else "deactivated"} successfully'
        })
    except Exception as e:
        logger.error(f"Error toggling vaccine status: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'An error occurred while updating the vaccine status'
        })

@login_required
def home(request):
    """Home page redirect"""
    if request.user.is_authenticated:
        return redirect('sysadmin:dashboard')
    return render(request, 'sysadmin/home.html')