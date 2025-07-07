from django.urls import path, include
from . import views

app_name='facilityadmin'


from Facilityadmin.views.healthcareW_view import (
    CreateHealthcareW,
    UpdateHealthcareW,
    ListHealthcareW,
    DeleteHealthcareW,
    
)
from Facilityadmin.views.facilityreport_view          import (
    ListFacilityReports,
    UploadFacilityReport
    )

urlpatterns = [
    path("create-healthcare-worker/", CreateHealthcareW.as_view(), name="create_healthcare_worker"),
    path("update-healthcare-worker/<str:worker_id>/", UpdateHealthcareW.as_view(), name="update_healthcare_worker"),
    path("list-healthcare-workers/", ListHealthcareW.as_view(), name="list_healthcare_workers"),
    path("delete-healthcare-worker/<str:worker_id>/", DeleteHealthcareW.as_view(), name="delete_healthcare_worker"),


    path("list-facility-reports/", ListFacilityReports.as_view(), name="list_facility_reports"),
    path("upload-facility-report/", UploadFacilityReport.as_view(), name="upload_facility_report"),
]