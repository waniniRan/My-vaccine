from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from Facilityadmin.models import FacilityReport, HealthcareW
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