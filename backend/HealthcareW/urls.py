from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .views import guardian_view, child_view, growthrecord_view, vaccinerecords_view
from .views import auth_view, guardian_self_view, growth_curve_view


app_name= 'healthcare'

urlpatterns = [
    # Authentication
    path('login/', auth_view.HealthcareWorkerLoginView.as_view(), name='healthcareworker-login'),
    path('change-password/', auth_view.HealthcareWorkerChangePasswordView.as_view(), name='healthcareworker-change-password'),
    # Guardian CRUD
    path('guardian/create/', guardian_view.CreateGuardian.as_view(), name='guardian-create'),
    path('guardian/list/', guardian_view.ListGuardian.as_view(), name='guardian-list'),
    path('guardian/update/<str:national_id>/', guardian_view.UpdateGuardian.as_view(), name='guardian-update'),
    path('guardian/delete/<str:national_id>/', guardian_view.DeleteGuardian.as_view(), name='guardian-delete'),
    # Child CRUD
    path('child/create/', child_view.CreateChild.as_view(), name='child-create'),
    path('child/list/', child_view.ListChild.as_view(), name='child-list'),
    path('child/update/<str:child_id>/', child_view.UpdateChild.as_view(), name='child-update'),
    path('child/delete/<str:child_id>/', child_view.DeleteChild.as_view(), name='child-delete'),
    # Growth Record CRUD
    path('growth-record/create/', growthrecord_view.CreateGrowthRecord.as_view(), name='growthrecord-create'),
    path('growth-record/list/', growthrecord_view.ListGrowthRecord.as_view(), name='growthrecord-list'),
    path('growth-record/update/<int:recordID>/', growthrecord_view.UpdateGrowthRecord.as_view(), name='growthrecord-update'),
    path('growth-record/delete/<int:recordID>/', growthrecord_view.DeleteGrowthRecord.as_view(), name='growthrecord-delete'),
    # Vaccination Record CRUD
    path('vaccination-record/create/', vaccinerecords_view.CreateVaccinationRecord.as_view(), name='vaccinationrecord-create'),
    path('vaccination-record/list/', vaccinerecords_view.ListVaccinationRecord.as_view(), name='vaccinationrecord-list'),
    path('vaccination-record/update/<str:recordID>/', vaccinerecords_view.UpdateVaccinationRecord.as_view(), name='vaccinationrecord-update'),
    path('vaccination-record/delete/<str:recordID>/', vaccinerecords_view.DeleteVaccinationRecord.as_view(), name='vaccinationrecord-delete'),
    # Guardian self-service endpoints
    path('guardian/login/', auth_view.GuardianLoginView.as_view(), name='guardian-login'),
    path('guardian/change-password/', auth_view.GuardianChangePasswordView.as_view(), name='guardian-change-password'),
    path('guardian/me/', guardian_self_view.GuardianProfileView.as_view(), name='guardian-profile'),
    path('guardian/children/', guardian_self_view.GuardianChildrenView.as_view(), name='guardian-children'),
    path('guardian/children/<str:child_id>/', guardian_self_view.GuardianChildDetailView.as_view(), name='guardian-child-detail'),
    path('guardian/children/<str:child_id>/growth/', guardian_self_view.GuardianChildGrowthView.as_view(), name='guardian-child-growth'),
    path('guardian/children/<str:child_id>/vaccines/', guardian_self_view.GuardianChildVaccinesView.as_view(), name='guardian-child-vaccines'),
    # Growth curve chart data
    path('growth-curve/<str:child_id>/', growth_curve_view.GrowthCurveView.as_view(), name='growth-curve'),
]