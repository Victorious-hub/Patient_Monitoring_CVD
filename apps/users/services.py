from datetime import datetime
import uuid
from django.db import transaction
from apps.treatment.models import Appointment
from apps.users.mixins import HandlerMixin
from apps.users.models import DoctorProfile, PatientProfile, CustomUser, Schedule
from django.contrib.auth.hashers import make_password
from apps.users.tasks import add_patient
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

        self._validate_credentials(self.user['password'], self.user['email'])
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
                 mobile: str = None,
                 address: str = None
                 ):
        self.mobile = mobile
        self.user = user
        self.address = address

    # @transaction.atomic
    # def patient_update_data(self, slug: str) -> PatientProfile:
    #     """Method to update patient data like common information
    #     """
    #     patient: PatientProfile = get_object(PatientProfile, slug=slug)

    #     patient.age = self.age
    #     patient.height = self.height
    #     patient.weight = self.weight
    #     patient.gender = self.gender
    #     patient.birthday = self.birthday

    #     patient.save()

    #     return patient

    @transaction.atomic
    def patient_update_contact(
        self,
        slug: str
    ) -> PatientProfile:
        """Method to update patient contact data like email or phone
        """
        patient: PatientProfile = get_object(PatientProfile, slug=slug)

        self._validate_mobile(self.mobile, patient.slug, slug)

        patient.mobile = self.mobile
        patient.address = self.address
        patient.user.first_name = self.user['first_name']
        patient.user.last_name = self.user['last_name']
        patient.user.save()
        patient.save()

        return patient


class DoctorService(HandlerMixin):
    def __init__(self,
                 doctor_slug: str = None,
                 appointment_date: datetime.date = None,
                 appointment_time: datetime.time = None,
                 user: CustomUser = None,
                 patients: PatientProfile = None,
                 profile_image: uuid = None
                 ):
        self.patients = patients
        self.user = user
        self.profile_image = profile_image
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.doctor_slug = doctor_slug

    @transaction.atomic
    def doctor_contact_update(
        self,
        slug: str
    ) -> DoctorProfile:
        """DoctorService's method for updating
        """

        doctor: DoctorProfile = get_object(DoctorProfile, slug=slug)

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
        doctor: DoctorProfile = get_object(DoctorProfile, slug=slug)

        doctor.patients.add(*self.patients)  # unpacking
        doctor.save()
        for i in self.patients:
            transaction.on_commit(
                lambda: add_patient.delay(slug, i.slug)
            )

        return doctor

    @transaction.atomic
    def patient_remove(
        self,
        slug: str
    ) -> DoctorProfile:
        """If patient is all right, or no need to give some treatment, delete him(her) from list
        """
        doctor: DoctorProfile = get_object(DoctorProfile, slug=slug)
        patient = self.patients

        if patient in doctor.patients.all():
            doctor.patients.remove(patient)
            doctor.save()

        return doctor

    @transaction.atomic
    def appointment_create(self, slug):
        doctor = get_object(DoctorProfile, slug=self.doctor_slug)
        patient = get_object(PatientProfile, slug=slug)
        schedule: Schedule = Schedule.objects.filter(available_time__has_key=self.appointment_date)
        if schedule:
            for i in schedule:
                i.available_time[self.appointment_date].remove(self.appointment_time)
                obj = Appointment.objects.create(
                    doctor=doctor,
                    patient=patient,
                    appointment_date=self.appointment_date,
                    appointment_time=self.appointment_time
                )

                obj.full_clean()
                obj.save()
                i.save()

                # transaction.on_commit(
                #     lambda: patient_appointment_creation.delay(slug, i.slug)
                # )

                return obj
