"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from Sysadmin.views.facility_view import CreateHealthFacility
from Sysadmin.views.facility_view import UpdateHealthFacility
from Sysadmin.views.facility_view import ListHealthFacility
from Sysadmin.views.facilityadmin_view import CreateFacilityAdmin
from Sysadmin.views.facilityadmin_view import UpdateFacilityAdmin
from Sysadmin.views.facilityadmin_view import ListFacilityAdmin
from Sysadmin.views.vaccine_view import CreateVaccine
from Sysadmin.views.vaccine_view import UpdateVaccine
from Sysadmin.views.vaccine_view import ListVaccine 



urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('api/', include('Sysadmin.urls')),
    path('api/',include('HealthcareW.urls')),
    path('api/', include('Facilityadmin.urls')),

#  URL for Sysadmin app
    # Include the URL for creating and handling health facilities
     path("create-facility/", CreateHealthFacility.as_view(), name="create_facility"),
     path("update-facility/", UpdateHealthFacility.as_view(), name="update_facility"),
     path("list-facilities/", ListHealthFacility.as_view(), name="list_facilities"),
    

    # Include the URL for creating and handling facility admins
    path("create-facility-admin/", CreateFacilityAdmin.as_view(), name="create_facility_admin"),
    path("update-facility-admin/", UpdateFacilityAdmin.as_view(), name="update_facility_admin"),
    path("list-facility-admins/", ListFacilityAdmin.as_view(), name="list_facility_admins"),

    # Include the URL for vaccine management
    path("create-vaccine/", CreateVaccine.as_view(), name="create_vaccine"),
    path("update-vaccine/", UpdateVaccine.as_view(), name="update_vaccine"),
    path("list-vaccines/", ListVaccine.as_view(), name="list_vaccines"),
]

