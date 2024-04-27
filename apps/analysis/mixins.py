from apps.users.exceptions import DoctorNotFound, PatientCardExists
from apps.users.models import DoctorProfile, PatientCard


class ValidationMixin:
    def _check_doctor_exists(self, slug: str):
        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

    def _card_exists(self, patient: str):
        if PatientCard.objects.filter(patient=patient).exists():
            raise PatientCardExists
