from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import HealthFacility, Vaccine

#USERADMIN
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
            return qs.filter(is_superuser=False)
        return qs
admin.site.register(User, CustomUserAdmin)
#END


#FACILITY_ADMIN & VACCINE
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'facility_type', 'admin')
    def save_model(self, request, obj, form, change):
        if not change:  # Only on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
admin.site.register(HealthFacility, FacilityAdmin)
admin.site.register(Vaccine)
#END