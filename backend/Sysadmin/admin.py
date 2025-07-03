from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Sysadmin.models.User import User
from Sysadmin.models.FacilityAdmin import FacilityAdmin
from Sysadmin.models.HealthFacility import HealthFacility
from Sysadmin.models.Vaccine import Vaccine


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_active')
    list_filter = ('role', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
          'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom Fields', {'fields': ('role', 'must_change_password')}),
    )
    add_fieldsets = (
       (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )



    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
         return qs
        return qs.filter(id=request.user.id)  # Limit to the logged-in user 
    
    def has_add_permission(self, request):
        # Only system admins can add users through Django admin
        return request.user.is_superuser and request.user.role == User.Role.SYSTEM_ADMIN
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Users can only edit their own profile
        return obj and obj.id == request.user.id
    
    def has_delete_permission(self, request, obj=None):
        # Only system admins can delete users
        return request.user.is_superuser and request.user.role == User.Role.SYSTEM_ADMIN
    
    def save_model(self, request, obj, form, change):
        if not change:  # New user
            # System admin can only create facility admins through Django admin
            if request.user.role == User.Role.SYSTEM_ADMIN:
                obj.role = User.Role.FACILITY_ADMIN
        super().save_model(request, obj, form, change)

class FacilityAdminAdmin(admin.ModelAdmin):
    """Facility Admin with restrictions"""
    list_display = ('admin_id', 'fullname', 'facility', 'is_active')
    list_filter = ('is_active', 'facility')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Facility admins can only see their own record
        if hasattr(request.user, 'facility_admin'):
            return qs.filter(id=request.user.facility_admin.id)
        return qs.none()
    
    def has_add_permission(self, request):
        # Only system admins can create facility admins
        return request.user.is_superuser and request.user.role == User.Role.SYSTEM_ADMIN
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Facility admins can edit their own profile
        return (hasattr(request.user, 'facility_admin') and 
                obj and obj.id == request.user.facility_admin.id)
    
    def has_delete_permission(self, request, obj=None):
        # Only system admins can delete facility admins
        return request.user.is_superuser and request.user.role == User.Role.SYSTEM_ADMIN

class HealthFacilityAdmin(admin.ModelAdmin):
    """Health Facility Admin with restrictions"""
    list_display = ('facility_id', 'facility_name', 'location', 'is_active')
    list_filter = ('is_active', 'facility_type')
    search_fields = ('facility_name', 'facility_id', 'location')
    readonly_fields = ('facility_id', 'prefix', 'created_at', 'updated_at')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Facility admins can only see their own facility
        if hasattr(request.user, 'facility_admin'):
            return qs.filter(id=request.user.facility_admin.facility.id)
        return qs.none()
    
    def has_add_permission(self, request):
        # Only system admins can create facilities
        return request.user.is_superuser and request.user.role == User.Role.SYSTEM_ADMIN
    
    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        # Facility admins can edit their own facility
        return (hasattr(request.user, 'facility_admin') and 
                obj and obj.id == request.user.facility_admin.facility.id)
    
    def has_delete_permission(self, request, obj=None):
        # Only system admins can delete facilities
        return request.user.is_superuser and request.user.role == User.Role.SYSTEM_ADMIN
    

class VaccineAdmin(admin.ModelAdmin):
    """Vaccine Admin - Only System Admin can manage"""
    list_display = ('vaccine_id', 'vaccine_name', 'vaccine_code', 'vaccine_type', 'status', 'expiry_date')
    list_filter = ('vaccine_type', 'status', 'manufacturer')
    search_fields = ('vaccine_name', 'vaccine_code', 'manufacturer')
    readonly_fields = ('vaccine_id', 'created_at', 'updated_at')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.none()  # Only system admins can see vaccines
    
    def has_add_permission(self, request):
        return request.user.is_superuser and request.user.role == User.Role.SYSTEM_ADMIN
    
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.user.role == User.Role.SYSTEM_ADMIN
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and request.user.role == User.Role.SYSTEM_ADMIN
    
    def save_model(self, request, obj, form, change):
        if not change:  # New vaccine
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(User, CustomUserAdmin)
admin.site.register(FacilityAdmin, FacilityAdminAdmin)
admin.site.register(HealthFacility, HealthFacilityAdmin)
admin.site.register(Vaccine, VaccineAdmin)
#END


