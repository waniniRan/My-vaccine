from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,generics,permissions
from .permissions import IsSystemAdmin
import csv,json
from datetime import timedelta
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import SystemReport,User,HealthFacility,Vaccine
from io import StringIO, BytesIO
from openpyxl import Workbook
from api.serializers import (HealthFacilitySerializer, VaccineSerializer,FacilityAdminCreationSerializer)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import FacilityAdminCreationForm, Vaccinationform




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
            address=serializer.validated_data.get('address', ''),
            admin=admin_user,
            created_by=request.user
        )

        # Return facility data with admin info
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

#LOGIN VIEWS
@login_required
@staff_member_required
def dashboard(request):
    context = {
        'facility_count': HealthFacility.objects.count(),
        'vaccine_count': Vaccine.objects.count(),
        'admin_count': User.objects.filter(role='FACILITY_ADMIN').count(),
        #'recent_logs': LogEntry.objects.all()[:10]  # Assuming you have a LogEntry model
    }
    return render(request, 'sysadmin/dashboard.html', context)

@login_required
@staff_member_required
def facilities(request):
    facilities = HealthFacility.objects.all()
    return render(request, 'sysadmin/facilities.html', {'facilities': facilities})

@login_required
@staff_member_required
def create_facility(request):
    if request.method == 'POST':
        form = FacilityAdminCreationForm(request.POST)
        if form.is_valid():
            # Process form data
            facility = form.save(commit=False)
            facility.created_by = request.user
            facility.save()
            return redirect('sysadmin:facilities')
    else:
        form = FacilityAdminCreationForm()
    
    return render(request, 'sysadmin/create_facility.html', {'form': form})


@login_required
@staff_member_required
def create_vaccine(request):
    if request.method == 'POST':
        form = Vaccinationform(request.POST)
        if form.is_valid():
            vaccine = form.save(commit=False)
            vaccine.created_by = request.user
            vaccine.save()
            
            # Handle ManyToMany field for facilities
            form.save_m2m()
            
            messages.success(request, f'Successfully created vaccine: {vaccine.name}')
            return redirect('sysadmin:vaccines')
    else:
        form = Vaccinationform()
    
    return render(request, 'sysadmin/create_vaccine.html', {'form': form})
@login_required
@staff_member_required
def vaccines(request):
    vaccines = Vaccine.objects.all()
    return render(request, 'sysadmin/vaccines.html', {'vaccines': vaccines})

@login_required
@staff_member_required
def facility_admin_detail(request, admin_id):
    admin = get_object_or_404(
        User.objects.select_related('managed_facility'),
        id=admin_id,
        role='FACILITY_ADMIN'
    )
    facility = admin.managed_facility
    
    context = {
        'admin': admin,
        'facility': facility,
        'last_login': admin.last_login.strftime('%Y-%m-%d %H:%M') if admin.last_login else 'Never'
    }
    return render(request, 'sysadmin/facility_admin_detail.html', context)




def create_facility_admin(request):
    if request.method == 'POST':
        form = FacilityAdminCreationForm(request.POST)
        if form.is_valid():
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
                admin=admin_user,
                 created_by=request.user
            )
            
            messages.success(request, f'Successfully created {facility.name} with admin {admin_user.username}')
            return redirect('sysadmin:facilities')
    else:
        form = FacilityAdminCreationForm()
    
    return render(request, 'sysadmin/create_facility_admin.html', {'form': form}) 