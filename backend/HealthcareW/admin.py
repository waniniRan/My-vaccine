from django.contrib import admin
from django.core.exceptions import PermissionDenied
from HealthcareW.models.GrowthCurve import GrowthCurve
from HealthcareW.models.Guardian import Guardian
from HealthcareW.models.Child import Child
from HealthcareW.models.VaccinationRecord import VaccinationRecord
from HealthcareW.models.GrowthRecord import GrowthRecord
from HealthcareW.models.Notification import Notification
from Sysadmin.models.User import User

# Register your models here.
class GrowthCurveAdmin(admin.ModelAdmin):
    """Growth Curve Admin - Only Healthcare Workers can manage"""
    list_display = ('child_id','curve_type', 'percentile', 'z_score', 'date_calculated', 'is_normal_range')
    list_filter = ('curve_type', 'is_normal_range', 'date_calculated')
    search_fields = ('child_id__first_name', 'child_id__last_name', 'curve_type')
    readonly_fields = ('percentile', 'z_score', 'date_calculated', 'is_normal_range')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'Worker'):
            return qs.filter(created_by=request.user)
        return qs.none()
    
    def has_add_permission(self, request):
        return (hasattr(request.user, 'Worker') and 
                request.user.role == User.Role.WORKER)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def has_delete_permission(self, request, obj=None):
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def save_model(self, request, obj, form, change):
#Automatically assign the logged-in healthcare worker as the creator."""
      if not change and hasattr(request.user, 'Worker'):
        obj.created_by = request.user
      super().save_model(request, obj, form, change)


class GuardianAdmin(admin.ModelAdmin):
    """Guardian Admin - Only Healthcare Workers can manage"""
    list_display = ('national_id', 'fullname', 'phone_number', 'email')
    search_fields = ('fullname', 'phone_number', 'email')
    readonly_fields = ('national_id',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'Worker'):
            return qs.filter(created_by=request.user)
        return qs.none()
    
    def has_add_permission(self, request):
        return (hasattr(request.user, 'Worker') and 
                request.user.role == User.Role.WORKER)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def has_delete_permission(self, request, obj=None):
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def save_model(self, request, obj, form, change):
        """Automatically assign the logged-in healthcare worker as the creator."""
        if not change and hasattr(request.user, 'Worker'):
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class ChildAdmin(admin.ModelAdmin):
    """Child Admin - Only Healthcare Workers can manage"""
    list_display = ('child_id', 'first_name', 'last_name', 'national_id', 'date_of_birth')
    list_filter = ('national_id', 'date_of_birth')
    search_fields = ('first_name', 'last_name', 'guardian__fullname')
    readonly_fields = ('child_id', 'national_id')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'Worker'):
            return qs.filter(created_by=request.user)
        return qs.none()
    def has_add_permission(self, request):
        return (hasattr(request.user, 'Worker') and 
                request.user.role == User.Role.WORKER)
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    def has_delete_permission(self, request, obj=None):
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    def save_model(self, request, obj, form, change):
        """Automatically assign the logged-in healthcare worker as the creator."""
        if not change and hasattr(request.user, 'Worker'):
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class VaccinationRecordAdmin(admin.ModelAdmin):
    """Vaccination Record Admin - Only Healthcare Workers can manage"""
    list_display = ('child_id', 'v_ID', 'administrationDate', 'doseNumber')
    list_filter = ('v_ID', 'administrationsDate')
    search_fields = ('child__first_name', 'child__last_name', 'name')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'Worker'):
            return qs.filter(created_by=request.user)
        return qs.none()
    
    def has_add_permission(self, request):
        return (hasattr(request.user, 'Worker') and 
                request.user.role == User.Role.WORKER)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def has_delete_permission(self, request, obj=None):
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def save_model(self, request, obj, form, change):
        """Automatically assign the logged-in healthcare worker as the creator."""
        if not change and hasattr(request.user, 'Worker'):
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class GrowthRecordAdmin(admin.ModelAdmin):
    """Growth Record Admin - Only Healthcare Workers can manage"""
    list_display = ('child_id', 'date_recorded', 'weight', 'height')
    list_filter = ('date_recorded', 'weight', 'height')
    search_fields = ('child__first_name', 'child__last_name')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'Worker'):
            return qs.filter(created_by=request.user)
        return qs.none()
    
    def has_add_permission(self, request):
        return (hasattr(request.user, 'Worker') and 
                request.user.role == User.Role.WORKER)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def has_delete_permission(self, request, obj=None):
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def save_model(self, request, obj, form, change):
        """Automatically assign the logged-in healthcare worker as the creator."""
        if not change and hasattr(request.user, 'Worker'):
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

class NotificationAdmin(admin.ModelAdmin):
    """Notification Admin - Only Healthcare Workers can manage"""
    list_display = ('notification_type', 'child_id', 'message', 'date_sent')
    list_filter = ('date_sent',)
    search_fields = ('child__first_name', 'child__last_name', 'message')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'Worker'):
            return qs.filter(created_by=request.user)
        return qs.none()
    
    def has_add_permission(self, request):
        return (hasattr(request.user, 'Worker') and 
                request.user.role == User.Role.WORKER)
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def has_delete_permission(self, request, obj=None):
        return (hasattr(request.user, 'Worker') and 
                obj and obj.created_by == request.user)
    
    def save_model(self, request, obj, form, change):
        """Automatically assign the logged-in healthcare worker as the creator."""
        if not change and hasattr(request.user, 'Worker'):
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

# Register the models with their respective admin classes
admin.site.register(GrowthCurve, GrowthCurveAdmin)  
admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(VaccinationRecord, VaccinationRecordAdmin)
admin.site.register(GrowthRecord, GrowthRecordAdmin)
admin.site.register(Notification, NotificationAdmin)