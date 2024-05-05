import pytest

from apps.users.models import DoctorProfile

@pytest.mark.django_db
def test_doctor_instance(doctor_factory):
    doctor = doctor_factory.build()
    assert isinstance(doctor, DoctorProfile)
    assert doctor.user.email == "test_doctor@gmail.com"
    assert doctor.user.is_staff is False
    assert doctor.user.role == "D"
