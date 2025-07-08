from rest_framework.permissions import BasePermission
from Sysadmin.models.User import User

class IsFacilityAdmin(BasePermission):
    """
    Allows access only to authenticated users with the Facility Admin role.
    """
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            hasattr(request.user, 'role') and
            request.user.role == User.Role.FACILITY_ADMIN and
            request.user.is_active
        )
