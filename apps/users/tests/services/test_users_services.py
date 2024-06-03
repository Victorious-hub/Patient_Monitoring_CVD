import pytest

from apps.users.exceptions import (
    EmailException, 
    MobileException, 
    PasswordLengthException
)
from apps.users.services import (
    PatientService, 
    RegistrationService
)


@pytest.mark.django_db
def test_patient_create_service(patient_factory):
    user_factory = patient_factory(
        first_name='John',
        last_name='Doe',
        email='johan@gmail.com',
        password='1234567890',
    )

    patient = RegistrationService(**user_factory)
    obj = patient.patient_create()
    assert obj.user.check_password('1234567890')
    assert obj.user.role == 'P'


@pytest.mark.django_db
def test_doctor_create_service(doctor_factory):
    doctor = doctor_factory(
        first_name='John',
        last_name='Doe',
        email='johan@gmail.com',
        password='123456890',
        description='Some data',
        experience=10,
    )

    obj = RegistrationService(**doctor).doctor_create()
    assert obj.user.check_password('123456890')
    assert obj.user.role == 'D'
    assert obj.profile_image != None
    assert obj.patients.count() == 0
    assert obj.patient_cards.count() == 0


@pytest.mark.django_db
def test_patient_create_email_exists_service(patient_factory):
    user_factory = patient_factory(
        first_name='John',
        last_name='Doe',
        email='johan@gmail.com',
        password='1234567890',
    )
    
    patient = RegistrationService(**user_factory)
    patient.patient_create()

    with pytest.raises(EmailException):
        patient.patient_create()


@pytest.mark.django_db
def test_patient_create_incorrect_password_service(patient_factory):
    user_factory = patient_factory(
        first_name='John',
        last_name='Doe',
        email='johan@gmail.com',
        password='1234',
    )
    
    patient = RegistrationService(**user_factory)
    with pytest.raises(PasswordLengthException):
        patient.patient_create()


@pytest.mark.django_db
def test_patient_update_service(patient_factory, patient_update_factory):
    user_factory = patient_factory(
        first_name='John',
        last_name='Doe',
        email='johan@gmail.com',
        password='123467890',
    )
    patient = RegistrationService(**user_factory).patient_create()

    patient_factory = patient_update_factory(
        first_name=patient.user.first_name,
        last_name=patient.user.last_name,
        address = 'Some address',
        mobile = '+1234567890',
    )

    patient_update = PatientService(**patient_factory).patient_update_contact(patient.slug)
    assert patient_update.mobile == '+1234567890'
    assert patient_update.address == 'Some address'


@pytest.mark.django_db
def test_patient_update_incorrect_mobile_service(patient_factory, patient_update_factory):
    user_factory = patient_factory(
        first_name='John',
        last_name='Doe',
        email='johan@gmail.com',
        password='123467890',
    )
    patient = RegistrationService(**user_factory).patient_create()

    patient_factory = patient_update_factory(
        first_name=patient.user.first_name,
        last_name=patient.user.last_name,
        address = 'Some address',
        mobile = '+12340',
    )

    with pytest.raises(MobileException):
        PatientService(**patient_factory).patient_update_contact(patient.slug)
