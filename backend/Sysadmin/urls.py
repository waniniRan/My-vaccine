from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from Sysadmin.views.facility_view import (CreateHealthFacility)
from Sysadmin.views.facility_view import ( UpdateHealthFacility)
from Sysadmin.views.facility_view import (ListHealthFacility)
from Sysadmin.views.facility_view import (DeleteHealthFacility)

from Sysadmin.views.facilityadmin_view import (
    CreateFacilityAdmin,
    UpdateFacilityAdmin,
    ListFacilityAdmin,
    DeleteFacilityAdmin,
)

from Sysadmin.views.vaccine_view import (
    CreateVaccine,
    UpdateVaccine,
    ListVaccine,
    DeleteVaccine,
)

# Import the new APIViews
from Sysadmin.views.user_view import UserListsView
from Sysadmin.views.report_view import SystemReportsView
from Sysadmin.views.activity_view import SystemActivityLogAPIView
from Sysadmin.views.facility_admin_auth import facility_admin_login
from Sysadmin.views.facility_admin_auth import facility_admin_change_password 
from Sysadmin.views.report_download_view import ReportDownloadView
from Sysadmin.views.report_export_view import SystemReportExportView

app_name = "Sysadmin"

urlpatterns = [
    # Facilities
    path("create-facility/", CreateHealthFacility.as_view(), name="create_facility"),
    path("update-facility/<str:ID>/", UpdateHealthFacility.as_view(), name="update_facility"),
    path("list-facilities/", ListHealthFacility.as_view(), name="list_facilities"),
    path("delete-facility/<str:ID>/", DeleteHealthFacility.as_view(), name="delete_facility"),

    # Facility Admins
    path("create-facility-admin/", CreateFacilityAdmin.as_view(), name="create_facility_admin"),
    path("update-facility-admin/<str:admin_id>/", UpdateFacilityAdmin.as_view(), name="update_facility_admin"),
    path("list-facility-admins/", ListFacilityAdmin.as_view(), name="list_facility_admins"),
    path("delete-facility-admin/<str:admin_id>/", DeleteFacilityAdmin.as_view(), name="delete_facility_admin"),
    path("facility-admin-login/", facility_admin_login),
    path("facility-admin-change-password/", facility_admin_change_password),



    # Vaccines
    path("create-vaccine/", CreateVaccine.as_view(), name="create_vaccine"),
    path("update-vaccine/<str:v_ID>/", UpdateVaccine.as_view(), name="update_vaccine"),
    path("list-vaccines/", ListVaccine.as_view(), name="list_vaccines"),
    path("delete-vaccine/<str:v_ID>/", DeleteVaccine.as_view(), name="delete-vaccine"),

    # System Admin APIs
    path("users/", UserListsView.as_view(), name="user-list"),
    path('system-reports/', SystemReportsView.as_view(), name="system-report-list"),
    path("system-activity-logs/", SystemActivityLogAPIView.as_view(), name="system-activity-log-list"),
    path('system-reports/<int:report_id>/download/', ReportDownloadView.as_view(), name='report-download'),
    path('system-reports/export/', SystemReportExportView.as_view(), name='report-export'),
]



