from rest_framework import permissions
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import logout
from Sysadmin.models.SystemReport import SystemReport
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
    
    
class RoleBasedAccessMiddleware:
    """Middleware to enforce role-based access"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            # Force password change if required
            if request.user.must_change_password and not request.path.startswith('/backend/'):
                return redirect('password_change')
            
            # Check if user is accessing appropriate sections
            if request.path.startswith('/admin/'):
                if not (request.user.is_staff or request.user.is_superuser):
                    logout(request)
                    return redirect('login')
        
        response = self.get_response(request)
        return response