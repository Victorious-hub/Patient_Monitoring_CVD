import pytest
import factory

from pytest_factoryboy import register
from faker import Factory as FakerFactory

from collections import OrderedDict
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
    }


@pytest.fixture
def user_service_invalid_password():
    user = OrderedDict(
        [
            ('email', "test1234@gmail.com"),
            ('first_name', factory.LazyFunction(lambda: faker.name())),
            ('last_name', "last_name"),
            ('is_staff', False),
            ('is_active', True),
            ('password', "1234567"),
        ]
    )
    return user


@pytest.fixture
def user_service_email_exists(user_service_invalid_password):
    user_service_invalid_password['password'] = "12345678"
    return user_service_invalid_password


register(CustomUserPatientFactory)
register(PatientFactory)
register(DoctorFactory)
register(CustomUserDoctorFactory)
register(CardFactory)
register(DoctorFactory1)

# some in built factory. Don't need to create in database
register(CardFactory, "patient_card")
