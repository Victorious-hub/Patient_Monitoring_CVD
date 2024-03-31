import pytest
import factory

from pytest_factoryboy import register
from faker import Factory as FakerFactory

from collections import OrderedDict
from apps.users.tests.factories import (
    CardFactory,
    CustomUserFactory,
    CustomUserFactory1,
    DoctorFactory,
    PatientFactory
)
from apps.investigations.tests.factories import (
    BloodInvestigationFactory,
    CholesterolInvestigationFactory,
    CustomTestFactory,
    CustomTestFactory1,
    PatientFactoryBlood,
    PatientFactoryCholesterol
)
faker = FakerFactory.create()


@pytest.fixture
def patient_service_invalid_password():
    user = OrderedDict(
        [
            ('email', "test1234@gmail.com"),
            ('first_name', factory.LazyFunction(lambda: faker.name())),
            ('last_name', "last_name"),
            ('is_staff', False),
            ('is_active', True),
            ('mobile', "+9034507810"),
            ('gender', "Male"),
            ('role', "P"),
            ('password', "1234567"),
        ]
    )
    return user


@pytest.fixture
def patient_service_email_exists():
    user = OrderedDict(
        [
            ('email', "test1234@gmail.com"),
            ('first_name', factory.LazyFunction(lambda: faker.name())),
            ('last_name', "last_name"),
            ('is_staff', False),
            ('is_active', True),
            ('mobile', "+9034507810"),
            ('gender', "Male"),
            ('role', "P"),
            ('password', "12345678"),
        ]
    )
    return user


@pytest.fixture
def patient_service_mobile_exists():
    user = OrderedDict(
        [
            ('email', "mail@gmail.com"),
            ('first_name', factory.LazyFunction(lambda: faker.name())),
            ('last_name', "last_name"),
            ('is_staff', False),
            ('is_active', True),
            ('mobile', "+903450781"),
            ('gender', "Male"),
            ('role', "P"),
            ('password', "12345678"),
        ]
    )
    return user


@pytest.fixture
def patient_service_update():
    email = "some_mail@gmail.com"
    user = OrderedDict(
        [
            ('email', email),
            ('first_name', factory.LazyFunction(lambda: faker.name())),
            ('last_name', "last_name"),
            ('is_staff', False),
            ('is_active', True),
            ('mobile', "+1234567890"),
            ('gender', "Male"),
            ('role', "P"),
            ('password', "12345678"),
            ('slug', email.split('@')[0]),
        ]
    )
    return user


register(CustomUserFactory)
register(PatientFactory)
register(DoctorFactory)
register(CustomUserFactory1)
register(CardFactory)

# some in built factory. Don't need to create in database
register(CardFactory, "patient_card")
register(CustomTestFactory)
register(CustomTestFactory1)
register(BloodInvestigationFactory)
register(CholesterolInvestigationFactory)
register(PatientFactoryBlood)
register(PatientFactoryCholesterol)
