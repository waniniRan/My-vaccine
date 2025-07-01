from rest_framework.permissions import BasePermission
from Sysadmin.models.User import User

class IsFacilityAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.User.Role == User.Role.FACILITY_ADMIN and
            request.user.is_active
        )

class IsFacilityAdminOrOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active
    
    def has_object_permission(self, request, view, obj):
        # Guardians can only access their own data
        if request.user.role == User.Role.GUARDIAN:
            return obj.guardian == request.user
        
        # Facility admins can access data from their facility
        elif request.user.role == User.Role.FACILITY_ADMIN:
            return obj.facility == request.user.facility
        
        # System admins can access everything
        elif request.user.role == User.Role.SYSTEM_ADMIN:
            return True
        
        return False