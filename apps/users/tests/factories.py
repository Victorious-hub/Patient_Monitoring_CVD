import factory
from apps.users.models import CustomUser, DoctorProfile, PatientCard, PatientProfile
from faker import Factory as FakerFactory

faker = FakerFactory.create()


class CustomUserPatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = 'test_patient@gmail.com'
    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = factory.LazyFunction(lambda: faker.name())
    password = '12345678'
    role = 'P'
    is_active = True
    is_staff = False


class CustomUserDoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = 'test_doctor@gmail.com'
    first_name = factory.LazyFunction(lambda: faker.name())
    last_name = factory.LazyFunction(lambda: faker.name())
    password = '12345678'
    role = 'D'
    is_active = True
    is_staff = False


class PatientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientProfile

    user = factory.SubFactory(CustomUserPatientFactory)
    slug = factory.LazyAttribute(lambda obj: obj.user.email.split('@')[0])
    weight = 25.0
    mobile = '+1122334455'
    height = 180
    age = 20
    gender = 'Male'
    birthday = '2020-10-10'


class CardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PatientCard

    patient = factory.SubFactory(PatientFactory)
    smoke = False
    alcohol = False
    active = True
    blood_type = factory.Faker('random_element', elements=['I', 'II', 'III', 'IV'])
    allergies = {'Pollen': 'pollen', 'Milk': 'milk'}
    abnormal_conditions = factory.LazyFunction(lambda: faker.name())


class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DoctorProfile
        skip_postgeneration_save = True

    user = factory.SubFactory(CustomUserDoctorFactory)
    slug = factory.LazyAttribute(lambda obj: obj.user.email.split('@')[0])
    # patients = factory.RelatedFactory(CustomUserPatientFactory) # ManyToMany
    # patient_cards = factory.RelatedFactory(CardFactory)


class DoctorFactory1(factory.django.DjangoModelFactory):
    class Meta:
        model = DoctorProfile
        skip_postgeneration_save = True

    user = factory.SubFactory(CustomUserDoctorFactory)
    slug = factory.LazyAttribute(lambda obj: obj.user.email.split('@')[0])
    patients = factory.RelatedFactory(PatientFactory)  # ManyToMany
    patient_cards = factory.RelatedFactory(CardFactory)
