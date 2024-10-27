from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated


class IsAdminUserWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks if the user has either is_staff=True or a role named "Admin".
    """
    def has_permission(self, request, view):
        return (request.user and request.user.is_staff) or (
            hasattr(request.user, 'role') and
            request.user.role and request.user.role.name == "Admin"
        )


class IsAdminOrAuthenticatedAndGET(permissions.BasePermission):
    """
    Permission that allows GET for authenticated users and makes every other method admin-only.
    """
    def has_permission(self, request, view):
        return (IsAuthenticated().has_permission(request, view) and request.method == "GET") or \
               IsAdminUserWithRole().has_permission(request, view)