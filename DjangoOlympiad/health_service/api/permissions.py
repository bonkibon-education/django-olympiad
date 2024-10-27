from rest_framework import permissions


class IsAdminUserWithRole(permissions.BasePermission):
    """
    Custom IsAdminUser permission that checks if the user has the role named "Admin".
    """

    def has_permission(self, request, view):
        # Check if the user has a role and if it is "Admin"
        return hasattr(request.user, 'role') and request.user.role and request.user.role.name == "Admin"


class IsAdminOrAuthenticatedAndGET(permissions.BasePermission):
    """
    Permission that allows access to the endpoint if one of the following conditions is true:

    - The user is an admin
    - The user is authenticated and the HTTP method is GET
    """

    def has_permission(self, request, view):
        # Allow access if the user is authenticated and making a GET request
        # or if the user has the "Admin" role
        return (
                (request.user and request.method == "GET" and request.user.is_authenticated) or
                (hasattr(request.user, 'role') and request.user.role and request.user.role.name == "Admin")
        )


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    Checks only if "user is not None"
    """

    def has_permission(self, request, view):
        # Checks if the user object is present, meaning the user is authenticated
        return request.user is not None
