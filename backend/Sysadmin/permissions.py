from rest_framework import permissions
from .models import User


class IsSystemAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role == User.Role.SYSTEM_ADMIN and
            request.user.is_active
        )



