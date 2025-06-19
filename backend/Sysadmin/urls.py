from django.urls import path
from . import views

app_name = 'sysadmin'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),  # or any view you're redirecting to
]