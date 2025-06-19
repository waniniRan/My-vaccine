from rest_framework import permissions
from .views import SystemReport
from datetime import timezone
from django.db import models

class ReportDownloadLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request, response):
        if '/api/reports/download/' in request.path:
            # Track download activity
            report_id = request.path.split('/')[-2]
            SystemReport.objects.filter(id=report_id).update(
                last_downloaded=timezone.now(),
                download_count=models.F('download_count') + 1
            )
        return response