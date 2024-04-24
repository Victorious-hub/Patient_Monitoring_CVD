
import re
from apps.users.exceptions import EmailException, MobileException, PasswordLengthException
from apps.users.models import CustomUser, DoctorProfile, PatientProfile


class HandlerMixin:
    PATTERN = r'^\+\d{10}$'

    def _validate_credentials(
        self,
        password: str,
        email: str,
        patient_slug: PatientProfile | DoctorProfile = None,
        slug: str = None
    ):
        if len(password) < 8:
            raise PasswordLengthException

        if CustomUser.objects.filter(email=email).exists():
            raise EmailException

        if CustomUser.objects.filter(email=email).exists() and patient_slug.slug != slug:
            raise EmailException

    def _validate_mobile(
        self,
        mobile: str,
        patient_slug: PatientProfile,
        slug: str
    ):
        if PatientProfile.objects.filter(mobile=mobile).exists() and patient_slug != slug \
                or not re.match(self.PATTERN, mobile):
            raise MobileException

    def _validate_update_data(
        self,
        email: str,
        patient_slug: PatientProfile,
        slug: str
    ):
        if CustomUser.objects.filter(email=email).exists() and patient_slug != slug:
            raise EmailException
