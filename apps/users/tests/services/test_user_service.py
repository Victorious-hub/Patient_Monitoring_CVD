import pytest

from apps.users.exceptions import EmailException, PasswordLengthException
from apps.users.services import RegistrationService


@pytest.mark.django_db
def test_user_create_invalid_password(user_service_invalid_password):
    patient = RegistrationService(user=user_service_invalid_password)

    with pytest.raises(PasswordLengthException):
        patient.patient_create()


@pytest.mark.django_db
def test_user_create_email_exists(user_service_email_exists):
    patient = RegistrationService(user=user_service_email_exists)
    assert patient.patient_create()

    with pytest.raises(EmailException):
        patient.patient_create()
