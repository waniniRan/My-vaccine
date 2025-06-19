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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from Sysadmin.views import SystemAdminDashboard,GenerateReportView, DownloadReportView,ReportListView
from Sysadmin.views import HealthFacilityListCreateView,HealthFacilityDetailView,CreateFacilityWithAdminView,VaccineListCreateView,VaccineDetailView
from Sysadmin.views import create_facility_admin, facility_admin_detail
from Sysadmin import views

app_name='sysadmin'

urlpatterns = [
    path('admin/', admin.site.urls),
    #System-admin URLS
    path('api/system-admin/dashboard/', SystemAdminDashboard.as_view(), name='system-admin-dashboard'),
    path('api/reports/generate/', GenerateReportView.as_view(), name='generate-report'),
    path('api/reports/download/<int:report_id>/', DownloadReportView.as_view(), name='download-report'),
    path('api/reports/list/', ReportListView.as_view(), name='list-reports'),

    #HEALTH FACILITY URLS
    path('health-facilities/', HealthFacilityListCreateView.as_view(), name='health-facility-list'),
    path('health-facilities/<int:pk>/', HealthFacilityDetailView.as_view(), name='health-facility-detail'),
    path('health-facilities/create-with-admin/', CreateFacilityWithAdminView.as_view(), name='create-facility-admin'),
    path('vaccines/', VaccineListCreateView.as_view(), name='vaccine-list'),
    path('vaccines/<int:pk>/', VaccineDetailView.as_view(), name='vaccine-detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('facilities/', views.facilities, name='facilities'),
    path('facilities/create/', views.create_facility, name='create_facility'),
    path('vaccines/create/', views.create_vaccine, name='create_vaccine'),  # Add this line
    path('vaccines/', views.vaccines, name='vaccines'),
    path('facilities/create-admin/', create_facility_admin, name='create_facility_admin'),
    path('facility-admins/<int:admin_id>/', facility_admin_detail, name='facility_admin_detail'),


    #Auth URLS
    path('sysadmin/', include('Sysadmin.urls', namespace= 'sysadmin')),
    path('login/', auth_views.LoginView.as_view(template_name='sysadmin/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name= 'logout'),
]



#path('facilities/<int:pk>/edit/', views.edit_facility, name='edit_facility'),
    #path('facilities/<int:pk>/delete/', views.delete_facility, name='delete_facility'),




