from django.contrib import admin
from django.core.exceptions import PermissionDenied
from Facilityadmin.models.HealthcareW import HealthcareW
from Sysadmin.models.User import User

# Register your models here.

class HealthcareWorkerAdmin(admin.ModelAdmin):
    """Healthcare Worker Admin with restrictions"""
    list_display = ('worker_id', 'fullname', 'position', 'facility', 'status')
    list_filter = ('status', 'position', 'facility')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Facility admins can only see workers in their facility
        if hasattr(request.user, 'facility_admin'):
            return qs.filter(facility=request.user.facility_admin.facility)
        return qs.none()
    
    def has_add_permission(self, request):
        # Only facility admins can create healthcare workers
        return (hasattr(request.user, 'facility_admin') and 
                request.user.role == User.Role.FACILITY_ADMIN)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Facility admins can edit workers in their facility
        return (hasattr(request.user, 'facility_admin') and 
                obj and obj.facility == request.user.facility_admin.facility)
    
    def has_delete_permission(self, request, obj=None):
        # Facility admins can delete workers in their facility
        return (hasattr(request.user, 'facility_admin') and 
                obj and obj.facility == request.user.facility_admin.facility)
    
    def save_model(self, request, obj, form, change):
        if not change:  # New worker
            if hasattr(request.user, 'facility_admin'):
                obj.facility = request.user.facility_admin.facility
                obj.Facility_admin = request.user.facility_admin
        super().save_model(request, obj, form, change)




admin.site.register(HealthcareW, HealthcareWorkerAdmin)
