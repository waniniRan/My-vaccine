from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from Sysadmin.views.facility_view import (CreateHealthFacility)
from Sysadmin.views.facility_view import ( UpdateHealthFacility)
from Sysadmin.views.facility_view import (ListHealthFacility)
from Sysadmin.views.facilityadmin_view import (
    CreateFacilityAdmin,
    UpdateFacilityAdmin,
    ListFacilityAdmin,
)
from Sysadmin.views.vaccine_view import (
    CreateVaccine,
    UpdateVaccine,
    ListVaccine,
)

app_name = "Sysadmin"

urlpatterns = [
    # Facilities
    path("create-facility/", CreateHealthFacility.as_view(), name="create_facility"),
    path("update-facility/<int:ID>/", UpdateHealthFacility.as_view(), name="update_facility"),
    path("list-facilities/", ListHealthFacility.as_view(), name="list_facilities"),

    # Facility Admins
    path("create-facility-admin/", CreateFacilityAdmin.as_view(), name="create_facility_admin"),
    path("update-facility-admin/<int:admin_id>/", UpdateFacilityAdmin.as_view(), name="update_facility_admin"),
    path("list-facility-admins/", ListFacilityAdmin.as_view(), name="list_facility_admins"),

    # Vaccines
    path("create-vaccine/", CreateVaccine.as_view(), name="create_vaccine"),
    path("update-vaccine/<int:v_id>/", UpdateVaccine.as_view(), name="update_vaccine"),
    path("list-vaccines/", ListVaccine.as_view(), name="list_vaccines"),
]



