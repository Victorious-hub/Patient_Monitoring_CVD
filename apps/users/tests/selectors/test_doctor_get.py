import pytest
from apps.users.models import DoctorProfile, PatientProfile
from apps.users.selectors import DoctorSelector


@pytest.mark.django_db
def test_doctor_retrieve(doctor_factory):
    user: DoctorProfile = doctor_factory.create()
    doctor = DoctorSelector()
    data = doctor.doctor_get(slug=user.slug)
    assert data


@pytest.mark.django_db
def test_doctor_patients_retrieve(doctor_factory):
    user: DoctorProfile = doctor_factory.create()
    doctor = DoctorSelector()
    data = doctor.doctor_get_patients(slug=user.slug)
    assert data


@pytest.mark.django_db
def test_patient_doctor_list(patient_factory):
    user: PatientProfile = patient_factory.build()
    doctor = DoctorSelector()
    data = doctor.doctor_list(slug=user.slug)
    assert data
