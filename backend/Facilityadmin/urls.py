from django.urls import path, include
from .views import FacilityReportViewSet, HealthcareWorkerViewSet
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'facility-reports', views.FacilityReportViewSet)
router.register(r'healthcare-workers', views.HealthcareWorkerViewSet)

app_name='facilityadmin'


urlpatterns = [
    # Facility Reports URLs
    path('facility-reports/', 
         views.FacilityReportViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='api_facility_reports_list'),
    
    path('facility-reports/<int:pk>/', 
         views.FacilityReportViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), 
         name='api_facility_report_detail'),
    
    path('facility-reports/<int:pk>/download/', 
         views.FacilityReportViewSet.as_view({'get': 'download'}), 
         name='api_download_report'),
    
    # Healthcare Workers URLs
    path('healthcare-workers/', 
         views.HealthcareWorkerViewSet.as_view({'get': 'list', 'post': 'create'}), 
         name='api_healthcare_workers_list'),
    
    path('healthcare-workers/<str:pk>/', 
         views.HealthcareWorkerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), 
         name='api_healthcare_worker_detail'),
    
    path('healthcare-workers/<str:pk>/activate/', 
         views.HealthcareWorkerViewSet.as_view({'post': 'activate'}), 
         name='api_activate_worker'),
    
    path('healthcare-workers/<str:pk>/deactivate/', 
         views.HealthcareWorkerViewSet.as_view({'post': 'deactivate'}), 
         name='api_deactivate_worker'),
]