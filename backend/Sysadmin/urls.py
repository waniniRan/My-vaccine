from django.urls import path, include
from django.contrib.auth import views as auth_views
from Sysadmin.views import HealthFacilityListCreateView,HealthFacilityDetailView,CreateFacilityWithAdminView,VaccineListCreateView,VaccineDetailView
from Sysadmin import views
from .views import HealthFacilityListCreateAPIView, HealthFacilityDetailAPIView,CreateFacilityWithAdminAPIView,ToggleFacilityStatusAPIView
from .views import LoginAPIView, LogoutAPIView, SystemAdminDashboardAPIView,VaccineDetailAPIView,VaccineListCreateAPIView
from .views import ToggleVaccineStatusAPIView,FacilityAdminListAPIView

app_name = 'sysadmin'

urlpatterns = [
   # Authentication
    path('auth/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    
    # Dashboard
    path('dashboard/', views.SystemAdminDashboardAPIView.as_view(), name='api_dashboard'),
    
    # Health Facilities
    path('facilities/', views.HealthFacilityListCreateAPIView.as_view(), name='facility_list_create'),
    path('facilities/<int:pk>/', views.HealthFacilityDetailAPIView.as_view(), name='facility_detail'),
    path('facilities/create-with-admin/', views.CreateFacilityWithAdminAPIView.as_view(), name='create_facility_with_admin'),
    path('facilities/<int:facility_id>/toggle-status/', views.ToggleFacilityStatusAPIView.as_view(), name='toggle_facility_status'),
    
    # Vaccines
    path('vaccines/', views.VaccineListCreateAPIView.as_view(), name='vaccine_list_create'),
    path('vaccines/<int:pk>/', views.VaccineDetailAPIView.as_view(), name='vaccine_detail'),
    path('vaccines/<int:vaccine_id>/toggle-status/', views.ToggleVaccineStatusAPIView.as_view(), name='toggle_vaccine_status'),
    
    # Users
    path('facility-admins/', views.FacilityAdminListAPIView.as_view(), name='facility_admin_list'),
    path('facility-admins/<int:pk>/', views.FacilityAdminDetailAPIView.as_view(), name='facility_admin_detail'),
    
    # Reports
    path('reports/generate/', views.GenerateReportAPIView.as_view(), name='generate_report'),
] 






