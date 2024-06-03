from django.http import Http404
import pytest
from apps.users.models import PatientProfile
from apps.users.selectors import PatientSelector


from apps.users.selectors import PatientSelector
from apps.users.services import RegistrationService


@pytest.mark.django_db
def test_patient_list(patient_factory):
    user_factory = patient_factory(
        first_name='John',
        last_name='Doe',
        email='johan@gmail.com',
        password='123467890',
    )
    RegistrationService(**user_factory).patient_create()
    data = PatientSelector().patient_list()
    assert len(data) > 0


# @pytest.mark.django_db
# def test_patient_retrieve(patient_factory):
#     user: PatientProfile = patient_factory.create()
#     patient = PatientSelector()
#     data = patient.patient_get(slug=user.slug)
#     assert data

#     with pytest.raises(Http404):
#         patient.patient_get(slug="unexisted patient instance")


# @pytest.mark.django_db
# def test_doctor_retrieve(doctor_factory):
#     user: DoctorProfile = doctor_factory.create()
#     doctor = DoctorSelector()
#     data = doctor.doctor_get(slug=user.slug)
#     assert data


# @pytest.mark.django_db
# def test_doctor_patients_retrieve(doctor_factory):
#     user: DoctorProfile = doctor_factory.create()
#     doctor = DoctorSelector()
#     data = doctor.doctor_get_patients(slug=user.slug)
#     assert data


# @pytest.mark.django_db
# def test_patient_doctor_list(patient_factory):
#     user: PatientProfile = patient_factory.build()
#     doctor = DoctorSelector()
#     data = doctor.doctor_list(slug=user.slug)
#     assert data
