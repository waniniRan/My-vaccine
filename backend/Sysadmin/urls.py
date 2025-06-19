from django.urls import path
from . import views

app_name = 'sysadmin'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('facilities/', views.facilities, name='facilities'),
    path('create-facility/', views.create_facility, name='create_facility'),
    path('create-vaccine/', views.create_vaccine, name='create_vaccine'),
    path('vaccines/', views.vaccines, name='vaccines'),
    path('create-facility-admin/', views.create_facility_admin, name='create_facility_admin'),
    path('facility-admin-detail/<int:admin_id>/', views.facility_admin_detail, name='facility_admin_detail'),
]
