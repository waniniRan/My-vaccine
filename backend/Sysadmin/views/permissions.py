from rest_framework.permissions import BasePermission
from Sysadmin.models.User import User
#from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from Sysadmin.models.User import User
from Sysadmin.models.FacilityAdmin import FacilityAdmin
from Sysadmin.models.HealthFacility import HealthFacility


class IsSystemAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role == User.Role.SYSTEM_ADMIN and
            request.user.is_active
        )

class IsSystemAdminOrOwner(BasePermission):
    """
    System admin can access everything, others only their own data
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active
    
    def has_object_permission(self, request, view, obj):
        # System admin can access everything
        if request.user.role == User.Role.SYSTEM_ADMIN:
            return True
        
        # Check if user owns the object (works for various models)
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'guardian'):
            return obj.guardian == request.user
        elif hasattr(obj, 'facility') and hasattr(request.user, 'facility'):
            return obj.facility == request.user.facility
        
        return False

class CanManageFacilities(BasePermission):
    """
    Only system admins can create/update/delete facilities
    """
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return (
                request.user.is_authenticated and 
                request.user.is_active and
                request.user.role in [User.Role.SYSTEM_ADMIN, User.Role.FACILITY_ADMIN]
            )
        
        return (
            request.user.is_authenticated and 
            request.user.role == User.Role.SYSTEM_ADMIN and
            request.user.is_active
        )

class CanManageUsers(BasePermission):
    """
    System admin can manage all users, facility admin can manage users in their facility
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_active and
            request.user.role in [User.Role.SYSTEM_ADMIN, User.Role.FACILITY_ADMIN]
        )
    
    def has_object_permission(self, request, view, obj):
        # System admin can manage all users
        if request.user.role == User.Role.SYSTEM_ADMIN:
            return True
        
        # Facility admin can only manage users in their facility
        elif request.user.role == User.Role.FACILITY_ADMIN:
            # Can't manage other system admins or facility admins
            if obj.role in [User.Role.SYSTEM_ADMIN, User.Role.FACILITY_ADMIN]:
                return False
            return obj.facility == request.user.facility
        
        return False


def is_system_admin(user):
    return user.is_authenticated and user.role == User.Role.SYSTEM_ADMIN

def is_facility_admin(user):
    return user.is_authenticated and user.role == User.Role.FACILITY_ADMIN

def is_healthcare_worker(user):
    return user.is_authenticated and user.role == User.Role.WORKER