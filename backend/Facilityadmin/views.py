from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import FacilityReport, HealthcareW
from api.serializers import (FacilityReportSerializer, HealthcareWorkerSerializer,HealthcareWorkerCreateSerializer)


class FacilityReportViewSet(viewsets.ModelViewSet):
    queryset = FacilityReport.objects.all()
    serializer_class = FacilityReportSerializer
    permission_classes = [IsAuthenticated]
    #filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ['facility', 'report_type', 'generated_by', 'is_downloaded']
    search_fields = ['facility__name', 'generated_by__first_name', 'generated_by__last_name']
    ordering_fields = ['generated_at', 'report_type']
    ordering = ['-generated_at']

    def get_queryset(self):
        # Filter reports based on user's facility access
        user = self.request.user
        if hasattr(user, 'Worker'):
            # Healthcare worker can only see reports from their facility
            return self.queryset.filter(facility=user.Worker.facility)
        elif hasattr(user, 'facility_admin'):
            # Facility admin can see reports from their managed facilities
            return self.queryset.filter(facility__in=user.facility_admin.facilities.all())
        return self.queryset  # Superuser or staff can see all

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        """Download report file and mark as downloaded"""
        report = get_object_or_404(FacilityReport, pk=pk)
        pass
        if report.report_file:
            # Mark as downloaded
            report.is_downloaded = True
            report.save()
            
            response = HttpResponse(
                report.report_file.read(),
                content_type='application/octet-stream'
            )
            response['Content-Disposition'] = f'attachment; filename="{report.report_file.name}"'
            return response
        
        return Response(
            {'error': 'No file attached to this report'},
            status=status.HTTP_404_NOT_FOUND
        )

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get report statistics"""
        queryset = self.get_queryset()
        
        stats = {
            'total_reports': queryset.count(),
            'downloaded_reports': queryset.filter(is_downloaded=True).count(),
            'pending_downloads': queryset.filter(is_downloaded=False).count(),
            'reports_by_type': {}
        }
        
        # Count reports by type
        for report_type, display_name in FacilityReport.REPORT_TYPES:
            count = queryset.filter(report_type=report_type).count()
            stats['reports_by_type'][report_type] = {
                'count': count,
                'display_name': display_name
            }
        
        return Response(stats)

class HealthcareWorkerViewSet(viewsets.ModelViewSet):
    queryset = HealthcareW.objects.all()
    permission_classes = [IsAuthenticated]
   # filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['facility', 'position', 'status', 'password_changed']
    search_fields = ['first_name', 'last_name', 'username', 'email', 'worker_id']
    ordering_fields = ['last_name', 'first_name', 'date_joined', 'created_at']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return HealthcareWorkerCreateSerializer
        return HealthcareWorkerSerializer

    def get_queryset(self):
        # Filter workers based on user's facility access
        user = self.request.user
        if hasattr(user, 'facility_admin'):
            # Facility admin can see workers from their managed facilities
            return self.queryset.filter(Facility_admin=user.facility_admin)
        elif hasattr(user, 'Worker'):
            # Healthcare worker can see colleagues from same facility
            return self.queryset.filter(facility=user.Worker.facility)
        return self.queryset  # Superuser or staff can see all

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate a healthcare worker"""
        worker = get_object_or_404(HealthcareW, pk=pk)
        worker.activate()
        serializer = self.get_serializer(worker)
        return Response({
            'message': f'{worker.get_full_name()} has been activated.',
            'worker': serializer.data
        })
        pass
    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Deactivate a healthcare worker"""
        worker = get_object_or_404(HealthcareW, pk=pk)
        worker.deactivate()
        
        serializer = self.get_serializer(worker)
        return Response({
            'message': f'{worker.get_full_name()} has been deactivated.',
            'worker': serializer.data
        })
        pass
    @action(detail=True, methods=['post'])
    def reset_password(self, request, pk=None):
        """Reset worker's password"""
        worker = get_object_or_404(HealthcareW, pk=pk)
        
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

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get worker statistics"""
        queryset = self.get_queryset()
        
        status = {
            'total_workers': queryset.count(),
            'active_workers': queryset.filter(status='active').count(),
            'inactive_workers': queryset.filter(status='inactive').count(),
            'suspended_workers': queryset.filter(status='suspended').count(),
            'workers_by_position': {},
            'pending_password_changes': queryset.filter(password_changed=False).count()
        }
        
        # Count workers by position
        for position, display_name in HealthcareW.Position_Choice:
            count = queryset.filter(position=position).count()
            stats['workers_by_position'][position] = {
                'count': count,
                'display_name': display_name
            }
        return stats(status)

    @action(detail=False, methods=['get'])
    def by_facility(self, request):
        """Get workers grouped by facility"""
        queryset = self.get_queryset()
        facility_param = request.query_params.get('facility_id')
        
        if facility_param:
            queryset = queryset.filter(facility_id=facility_param)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
