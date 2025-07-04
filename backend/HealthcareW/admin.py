from django.contrib import admin
from django.core.exceptions import PermissionDenied
from HealthcareW.models.GrowthCurve import GrowthCurve
from HealthcareW.models.Guardian import Guardian
from HealthcareW.models.Child import Child
from HealthcareW.models.VaccinationRecord import VaccinationRecord
from HealthcareW.models.GrowthRecord import GrowthRecord
from HealthcareW.models.Notification import Notification
from Sysadmin.models.User import User
from django.contrib.admin import AdminSite

# Register your models here.
# backend/healthcareworker_admin.py



class HealthWorkerAdminSite(AdminSite):
    site_header = "Healthcare Worker Dashboard"
    site_title = "Healthcare Worker Portal"
    index_title = "Welcome to the Healthcare Worker Portal"

    def has_permission(self, request):
        return request.user.is_active and request.user.groups.filter(name='HealthcareWorker').exists()

healthworker_admin_site = HealthWorkerAdminSite(name='healthworker')

from django.contrib import admin

class OwnDataOnlyAdmin(admin.ModelAdmin):
    """
    Limits records to objects created by this health worker
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        if obj:
            return obj.created_by == request.user
        return True

    def has_delete_permission(self, request, obj=None):
        if obj:
            return obj.created_by == request.user
        return True

    def has_add_permission(self, request):
        return True


# register with restricted permissions:
healthworker_admin_site.register(Guardian, OwnDataOnlyAdmin)
healthworker_admin_site.register(Child, OwnDataOnlyAdmin)
healthworker_admin_site.register(GrowthRecord, OwnDataOnlyAdmin)
healthworker_admin_site.register(GrowthCurve, OwnDataOnlyAdmin)
healthworker_admin_site.register(VaccinationRecord, OwnDataOnlyAdmin)
healthworker_admin_site.register(Notification, OwnDataOnlyAdmin)
