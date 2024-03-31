import pytest
from apps.users.models import CustomUser, DoctorProfile, PatientProfile


@pytest.mark.django_db
def test_custom_user_model(custom_user_factory):
    user = custom_user_factory.create()
    assert user.email == "test@gmail.com"


@pytest.mark.django_db
def test_custom_user_instance(custom_user_factory):
    user = custom_user_factory.build()
    assert isinstance(user, CustomUser)


@pytest.mark.django_db
def test_patient_model(patient_factory):
    patient = patient_factory.create()
    assert patient.user.email == "test@gmail.com"
    assert patient.user.is_staff is False
    assert patient.user.role == "P"


@pytest.mark.django_db
def test_doctor_model(doctor_factory):
    doctor = doctor_factory.create()
    assert doctor.user.email == "test1@gmail.com"
    assert doctor.user.is_staff is False
    assert doctor.user.role == "D"


@pytest.mark.django_db
def test_patient_instance(patient_factory):
    patient = patient_factory.build()
    assert isinstance(patient, PatientProfile)


@pytest.mark.django_db
def test_doctor_instance(doctor_factory):
    doctor = doctor_factory.build()
    assert isinstance(doctor, DoctorProfile)
