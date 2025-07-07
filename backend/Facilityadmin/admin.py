from django.contrib.admin import AdminSite
from Facilityadmin.models.HealthcareW import HealthcareW
from Sysadmin.models.FacilityAdmin import FacilityAdmin
from HealthcareW.models.Notification import Notification
from Sysadmin.models.User import User
from django.contrib import admin
from Facilityadmin.models.FacilityReport import FacilityReport

class FacilityAdminSite(AdminSite):
    site_header = "Facility Administration"
    site_title = "Facility Admin Portal"
    index_title = "Welcome to the Facility Admin Portal"

    def has_permission(self, request):
        return request.user.is_active and request.user.groups.filter(name="FacilityAdmin").exists()

facility_admin_site = FacilityAdminSite(name='facilityadmin')

from django.contrib import admin

class HealthcareWorkerAdmin(admin.ModelAdmin):
    """
    Facility admins can manage healthcare workers within their own facility
    """
    list_display = ('worker_id', 'fullname', 'position', 'facility', 'status')
    list_filter = ('status', 'position', 'facility')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(facility=request.user.facilityadmin.facility)

    def has_add_permission(self, request):
        return (hasattr(request.user, 'facilityadmin') and 
                request.user.groups.filter(name='FacilityAdmin').exists())

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return (hasattr(request.user, 'facilityadmin') and 
                obj and obj.facility == request.user.facilityadmin.facility)

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)
    


@admin.register(FacilityReport)
class FacilityReportAdmin(admin.ModelAdmin):
    list_display = (
        "id", "facility", "report_type", "generated_by", "generated_at", "is_downloaded")
    search_fields = ("facility__name", "report_type")
    list_filter = ("report_type", "facility")

facility_admin_site.register(FacilityReport, FacilityReportAdmin)
facility_admin_site.register(HealthcareW, HealthcareWorkerAdmin)
facility_admin_site.register(Notification, admin.ModelAdmin)
facility_admin_site.register(FacilityAdmin, admin.ModelAdmin)
facility_admin_site.register(User, admin.ModelAdmin)
