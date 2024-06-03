import pytest
from apps.users.selectors import DoctorSelector, PatientSelector

from apps.users.services import RegistrationService


@pytest.fixture
def user_patient_model(patient_factory):
    user_factory = patient_factory(
        first_name='John',
        last_name='Doe',
        email='johan@gmail.com',
        password='123467890',
    )
    patient = RegistrationService(**user_factory).patient_create()
    return patient


@pytest.fixture
def doctor_user_model(doctor_factory):
    user_factory = doctor_factory(
        first_name='John',
        last_name='Doe',
        email='johan@gmail.com',
        password='123467890',
        description='some data',
        experience=10,
    )
    doctor = RegistrationService(**user_factory).doctor_create()
    return doctor


@pytest.mark.django_db
def test_patient_list(user_patient_model):
    data = PatientSelector().patient_list()
    assert data is not None
    assert len(data) != 0


@pytest.mark.django_db
def test_patient_retrieve(user_patient_model):
    data = PatientSelector().patient_get(
        slug=user_patient_model.user.email.split('@')[0]
    )
    assert data


@pytest.mark.django_db
def test_patient_incorrect_slug(user_patient_model):
    data = PatientSelector().patient_get(
        slug=user_patient_model.user.email.split('@')[1]
    )
    assert data is None


@pytest.mark.django_db
def test_doctor_list(doctor_user_model):
    data = DoctorSelector().doctor_list()
    assert data is not None
    assert len(data) != 0


@pytest.mark.django_db
def test_doctor_retrieve(doctor_user_model):
    data = DoctorSelector().doctor_get(
        slug=doctor_user_model.user.email.split('@')[0]
    )
    assert data
