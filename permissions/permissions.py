from rest_framework import permissions
from staffs.models import Staff

from permissions.utils import verify_request_kwargs


class CreationPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if not (
            request.user.is_superuser
            or request.user.is_manager
            or request.user.is_staff
        ):
            return False

        return True


# Permissões para update e delete de owners


class RUDOwnerPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method == "DELETE":
            if not (request.user.is_superuser or request.user.is_manager):
                return False

        if request.method in ["PATCH", "PUT"]:
            if not (
                request.user.is_superuser
                or request.user.is_manager
                or request.user.is_staff
            ):
                return False
        return True


class StoreCRUDPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_superuser:
            return False

        return True


class StaffCRUDPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if not (request.user.is_superuser or request.user.is_manager):
            return False

        if request.user.is_superuser:
            return True

        kwarg_user = verify_request_kwargs(request, Staff)

        if request.user.is_manager and kwarg_user.is_superuser:
            return False

        return True


class StaffCreationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if not (request.user.is_superuser or request.user.is_manager):
            return False

        if request.user.is_superuser:
            return True

        return True


class PetsCRUDPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if request.method == "POST":
            if not (
                request.user.is_superuser
                or request.user.is_manager
                or request.user.is_staff
            ):
                return False

        if request.method == "DELETE":
            if not (request.user.is_superuser or request.user.is_manager):
                return False

        return True


class ReportsCRUDPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if not (
            request.user.is_superuser
            or request.user.is_manager
            or request.user.is_doctor
        ):
            return False

        return True


class ServicesCRUDPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if not (request.user.is_superuser or request.user.is_manager):
            return False

        return True


class FinancialReportsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.is_superuser or request.user.is_manager:
            return False

        return True
