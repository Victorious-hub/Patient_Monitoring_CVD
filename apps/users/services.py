from datetime import datetime
from django.db import transaction
from apps.users.mixins import HandlerMixin
from apps.users.models import DoctorProfile, PatientProfile, CustomUser
from django.contrib.auth.hashers import make_password
from apps.users.tasks import doctor_patient_add
from apps.users.utils import get_object


class RegistrationService(HandlerMixin):
    def __init__(self,
                 user: CustomUser = None,
                 ):
        self.user = user

    def create_user(self, user_data, role):
        new_user = CustomUser.objects.create(
            **user_data,
            role=role
        )
        new_user.password = make_password(new_user.password)
        new_user.save()
        return new_user

    @transaction.atomic
    def doctor_create(self) -> DoctorProfile:
        """DoctorService's method to create doctor instance
        """

        self._validate_credentials()
        user = self.create_user(self.user, role='D')

        obj = DoctorProfile.objects.create(user=user)
        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def patient_create(self) -> PatientProfile:
        """Method to create a patient instance
        """

        self._validate_credentials(self.user['password'], self.user['email'])
        user = self.create_user(self.user, role='P')

        obj = PatientProfile.objects.create(user=user)
        obj.full_clean()
        obj.save()

        return obj


class PatientService(HandlerMixin):
    def __init__(self,
                 user: CustomUser = None,
                 weight: float = None,
                 height: int = None,
                 gender: str = None,
                 birthday: datetime = None,
                 age: int = None,
                 mobile: str = None,
                 ):
        self.mobile = mobile
        self.user = user
        self.weight = weight
        self.height = height
        self.age = age
        self.birthday = birthday
        self.gender = gender

    @transaction.atomic
    def patient_update_data(self, slug: str) -> PatientProfile:
        """Method to update patient data like common information
        """
        patient = get_object(PatientProfile, slug=slug)

        patient.age = self.age
        patient.height = self.height
        patient.weight = self.weight
        patient.gender = self.gender
        patient.birthday = self.birthday

        patient.save()

        return patient

    @transaction.atomic
    def patient_update_contact(
        self,
        slug: str
    ) -> PatientProfile:
        """Method to update patient contact data like email or phone
        """
        patient = get_object(PatientProfile, slug=slug)

        self._validate_mobile(self.mobile, patient.slug, slug)
        self._validate_update_data(patient.user.email, patient.slug, slug)

        patient.mobile = self.mobile
        patient.user.first_name = self.user['first_name']
        patient.user.last_name = self.user['last_name']
        patient.user.email = self.user['email']
        patient.user.save()
        patient.save()

        return patient


class DoctorService(HandlerMixin):
    def __init__(self,
                 user: CustomUser = None,
                 patients: PatientProfile = None,
                 ):
        self.patients = patients
        self.user = user

    @transaction.atomic
    def doctor_contact_update(
        self,
        slug: str
    ) -> DoctorProfile:
        """DoctorService's method for updating
        """

        doctor = get_object(DoctorProfile, slug=slug)
        self._validate_update_data(doctor.user.email, doctor.slug, slug)

        doctor.user.email = self.user['email']
        doctor.user.first_name = self.user['first_name']
        doctor.user.last_name = self.user['last_name']
        doctor.user.save()

        return doctor

    @transaction.atomic
    def patient_list_update(
        self,
        slug: str,
    ) -> DoctorProfile:
        """Method to add patients to doctor's current list of patients
        """
        doctor = get_object(DoctorProfile, slug=slug)

        doctor.patients.add(*self.patients)  # unpacking
        doctor.save()

        transaction.on_commit(
            lambda: doctor_patient_add.delay(slug)
        )

        return doctor

    @transaction.atomic
    def patient_remove(
        self,
        slug: str
    ) -> DoctorProfile:
        """If patient is all right, or no need to give some treatment, delete him(her) from list
        """
        doctor = get_object(DoctorProfile, slug=slug)
        patient = self.patients

        if patient in doctor.patients.all():
            doctor.patients.remove(patient)
            doctor.save()

        return doctor
