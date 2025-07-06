#from rest_framework import permissions
#from django.shortcuts import redirect
#from django.urls import reverse
#from django.contrib.auth import logout
#from Sysadmin.models.SystemReport import SystemReport
#from datetime import timezone
#from django.db import models

# middleware.py (create this file in your app)
import logging

logger = logging.getLogger(__name__)

class AuthDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Debug authentication headers
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        print(f"Request path: {request.path}")
        print(f"Auth header: {auth_header}")
        print(f"Request user: {request.user}")
        print(f"Is authenticated: {request.user.is_authenticated if hasattr(request.user, 'is_authenticated') else 'Unknown'}")
        
        response = self.get_response(request)
        return response

# Add to MIDDLEWARE in settings.py (temporarily for debugging)
MIDDLEWARE = [
    # ... other middleware
    'your_app.middleware.AuthDebugMiddleware',  # Add this temporarily
    # ... rest of middleware
]