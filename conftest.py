import pytest
from django.contrib.auth.hashers import make_password

from pytest_factoryboy import register
from faker import Factory as FakerFactory

from collections import OrderedDict
from apps.users.models import CustomUser, DoctorProfile, PatientCard, PatientProfile
from apps.users.tests.factories import (
    CardFactory,
    CustomUserPatientFactory,
    CustomUserDoctorFactory,
    DoctorFactory,
    PatientFactory,
    DoctorFactory1
)
import medtech

faker = FakerFactory.create()


@pytest.fixture(scope='session')
def django_db_setup():
    medtech.django.base.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'user-name',
        'HOST': 'db',
        'PORT': 5432,
        'PASSWORD': 'strong-password',
        'ATOMIC_REQUESTS': True,
    }



@pytest.fixture
def patient_factory(db):
    def create_app_patient(
            email: str = None,
            first_name: str = None,
            last_name: str = None,
            password: str = None,
    ):
        patient_data = {
            'user': {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
            },
        }
        return patient_data
    return create_app_patient

@pytest.fixture
def doctor_factory(db):
    def create_app_doctor(
            email: str = None,
            first_name: str = None,
            last_name: str = None,
            password: str = None,
            description: str = None,
            experience: int = None,
    ):
        doctor_data = {
            'user': {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'password': password,
            },
            'description': description,
            'experience': experience,
        }
        return doctor_data
    return create_app_doctor


@pytest.fixture
def patient_update_factory(db):
    def create_app_patient(
            first_name: str = None,
            last_name: str = None,
            address: str = None,
            mobile: str = None,
    ):
        patient_data = {
            'user': {
                'first_name': first_name,
                'last_name': last_name,
            },
            'address': address,
            'mobile': mobile,
        }
        return patient_data
    return create_app_patient


register(CustomUserPatientFactory)
register(PatientFactory)
register(DoctorFactory)
register(CustomUserDoctorFactory)
register(CardFactory)
register(DoctorFactory1)

# some in built factory. Don't need to create in database
register(CardFactory, "patient_card")
