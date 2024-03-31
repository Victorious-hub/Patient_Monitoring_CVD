import factory
import uuid
from apps.users.models import CustomUser, DoctorProfile, PatientCard, PatientProfile
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = 'test@gmail.com'
    is_staff = 'True'
    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = 'last_name'
    password = '12345678'
    mobile = '+1122334455'
    role = 'P'
    gender = 'Male'
    is_active = True
    is_staff = False


class CustomUserFactory1(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = 'test1@gmail.com'
    is_staff = 'True'
    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = 'last_name'
    password = '12345678'
    mobile = '+1234567890'
    role = 'D'
    gender = 'Male'
    is_active = True
    is_staff = False


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientProfile

    user = factory.SubFactory(CustomUserFactory)
    slug = factory.LazyAttribute(lambda obj: obj.user.email.split('@')[0])
    address = factory.LazyFunction(lambda: faker.sentence(nb_words=10))


class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DoctorProfile
        skip_postgeneration_save = True

    user = factory.SubFactory(CustomUserFactory1)
    slug = factory.LazyAttribute(lambda obj: obj.user.email.split('@')[0])
    spec = 'D'
    patients = factory.RelatedFactory(PatientFactory)


class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientCard

    doctor_owners = factory.SubFactory(DoctorFactory)
    patient = factory.SubFactory(PatientFactory)
    height = 180
    weight = 87.5
    age = factory.Faker('random_int', min=1, max=100)
    is_smoking = 'No'
    is_alcohol = 'No'
    card_id = factory.LazyFunction(uuid.uuid4)
    blood_type = factory.Faker('random_element', elements=['A', 'B', 'AB', 'O'])
    allergies = 'Pollen'
    ex_conditions = 'sentence'
