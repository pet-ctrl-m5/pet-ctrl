from rest_framework import permissions


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
