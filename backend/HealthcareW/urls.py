from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views


app_name= 'healthcare'

urlpatterns = [
    path('auth/login/', views.CustomTokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('guardian/children/', views.guardian_children),
    path('children/<int:child_id>/', views.child_detail),
    path('children/<int:child_id>/vaccinations/', views.child_vaccinations),
    path('children/<int:child_id>/growth-data/', views.child_growth_data),
    path('notifications/', views.notifications),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read),
]