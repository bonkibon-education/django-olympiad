import logging

from django.shortcuts import get_object_or_404
from rest_framework import permissions

from .models import Visit
from .grpc_consume_produce import grpc_check_roles  # Подключение grpc_check_roles для использования в grpc_check_user_and_role

def grpc_check_user_and_role(user_id, role):
    """
    Проверяет, имеет ли пользователь указанную роль с помощью gRPC.
    """
    user, is_valid = grpc_check_roles(user_id, role)
    return user, is_valid

class IsAdminOrManagerOrDoctorWithRole(permissions.BasePermission):
    """
    Checks if the user has the role "Admin", "Manager", or "Doctor".
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role and request.user.role.name in ["Admin", "Manager", "Doctor"]


class IsAdminOrManagerWithRole(permissions.BasePermission):
    """
    Checks if the user has the role "Admin" or "Manager".
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role and request.user.role.name in ["Admin", "Manager"]


class IsDoctorWithRole(permissions.BasePermission):
    """\\\
    Checks if the user has the role "Doctor".
    - Even pure admins can't pass this permission.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role and request.user.role.name == "Doctor"


class IsDoctorOrPatientWithRole(permissions.BasePermission):
    """
    Checks if the user has the role "Doctor" or "User".
    - Even pure admins can't pass this permission.
    """

    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.role and request.user.role.name in ["Doctor", "User"]


class IsDoctorOrLinkedPatientToVisit(permissions.BasePermission):
    """
    Allows access to Visits if the user is a doctor or the patient linked to the specified Visit.
    """

    def has_permission(self, request, view):
        if request.user is None:
            return False

        visit_id = request.parser_context['kwargs'].get("id")
        instance = Visit.objects.filter(id=visit_id).first()
        if instance:
            return instance.patient_id == request.user.id or (hasattr(request.user, 'role') and request.user.role.name == "Doctor")
        return False


class IsDoctorOrGivenPatient(permissions.BasePermission):
    """
    Allows viewing history by patient ID if the user is a doctor or the specified patient.
    """

    def has_permission(self, request, view):
        patient_id = request.parser_context['kwargs'].get("id")
        patient, is_valid = grpc_check_user_and_role(patient_id, 'User')
        if not is_valid:
            return False

        return patient.id == request.user.id or (hasattr(request.user, 'role') and request.user.role.name == "Doctor")


class GetPutVisitByIdPermission(permissions.BasePermission):
    """
    Special permission: if GET, check `IsDoctorOrLinkedPatientToVisit`; otherwise, `IsAdminOrManagerWithRole`.
    """

    def has_permission(self, request, view):
        logging.debug(
            f"Request Method: {request.method}, "
            f"IsDoctorOrLinkedPatientToVisit: {IsDoctorOrLinkedPatientToVisit().has_permission(request, view)}, "
            f"IsAdminOrManagerWithRole: {IsAdminOrManagerWithRole().has_permission(request, view)}"
        )

        if request.method == "GET":
            return IsDoctorOrLinkedPatientToVisit().has_permission(request, view)
        else:
            return IsAdminOrManagerWithRole().has_permission(request, view)
