from rest_framework import permissions
from .models import Appointment


class IsAdminOrManagerWithRole(permissions.BasePermission):
    """
    Custom permission that checks if the user's role is either "Admin" or "Manager".
    """

    def has_permission(self, request, view):
        # Check if the user has a role and if it is "Admin" or "Manager"
        if request.user.role:
            return request.user.role.name in ["Admin", "Manager"]
        return False


class IsAdminOrManagerOrDoctorWithRole(permissions.BasePermission):
    """
    Custom permission that checks if the user's role is "Admin", "Manager", or "Doctor".
    """

    def has_permission(self, request, view):
        # Check if the user has a role and if it is "Admin", "Manager", or "Doctor"
        if request.user.role:
            return request.user.role.name in ["Admin", "Manager", "Doctor"]
        return False


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user is not None


class DeleteAppointmentPermission(permissions.BasePermission):
    """
    Permission to delete an appointment: only an admin/manager or the user assigned to the appointment.
    """

    def has_permission(self, request, view):
        # Check if user is authenticated and has the role of "Admin" or "Manager"
        if request.user is not None and request.user.role:
            if request.user.role.name in ["Admin", "Manager"]:
                return True
            # Check if the user is the one who created the appointment
            appointment = Appointment.objects.filter(
                id=request.parser_context['kwargs'].get("id"),
                user_id=request.user.id
            )
            if appointment.exists():
                return True
        return False


class IsAdminOrManagerWithRoleOrGetAndAuthenticated(permissions.BasePermission):
    """
    Allows GET requests for authenticated users and restricts other methods to users with "Admin" or "Manager" roles.
    """

    def has_permission(self, request, view):
        # Allow GET requests for any authenticated user
        if request.user is not None:
            if request.method == "GET":
                return True
            # Allow other requests if the user has the role of "Admin" or "Manager"
            if request.user.role and request.user.role.name in ["Admin", "Manager"]:
                return True
        return False
