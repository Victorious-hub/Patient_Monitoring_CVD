import pytest

from apps.users.models import PatientProfile


@pytest.mark.django_db
def test_patient_instance(patient_factory):
    patient = patient_factory.build()
    assert isinstance(patient, PatientProfile)
    assert patient.user.email == "test_patient@gmail.com"
    assert patient.user.is_staff is False
    assert patient.user.role == "P"
