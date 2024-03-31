from rest_framework.permissions import BasePermission


class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        doctor = request.user.role
        is_true = (doctor == "D")
        return bool(request.user and is_true and request.user.is_authenticated)


class IsPatient(BasePermission):
    def has_permission(self, request, view):
        patient = request.user.role
        is_true = (patient == "P" or patient == "D")
        return bool(is_true and request.user.is_authenticated)
