from rest_framework.permissions import BasePermission


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        patient = request.user.role
        is_true = (patient == "P")
        return bool(is_true and request.user.is_authenticated)
