import uuid
from datetime import datetime
from django.db import transaction
from apps.treatment.models import Appointment
from .mixins import UserValidationMixin
from apps.users.utils import get_object
from django.contrib.auth.hashers import make_password
from apps.users.models import DoctorProfile, PatientProfile, CustomUser
from apps.users.tasks import patient_add_task, consulting_appointment_task


class RegistrationService(UserValidationMixin):
    def __init__(self,
                 user: CustomUser = None,
                 experience: int = None,
                 description: str = None
                 ):
        self.user = user
        self.description = description
        self.experience = experience

    @transaction.atomic
    def create_user(self, user_data, role):
        """Create CustomUser instance method
        """
        new_user = CustomUser.objects.create(
            **user_data,
            role=role
        )
        new_user.password = make_password(new_user.password)
        new_user.save()
        return new_user

    @transaction.atomic
    def doctor_create(self) -> DoctorProfile:
        """Create DoctorProfile instance method with CustomUser instance
        """
        self._validate_credentials(self.user['password'], self.user['email'])
        user = self.create_user(self.user, role='D')

        obj = DoctorProfile.objects.create(
            user=user,
            experience=self.experience,
            description=self.description
        )
        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def patient_create(self) -> PatientProfile:
        """Create PatientProfile instance method with CustomUser instance
        """

        self._validate_credentials(self.user['password'], self.user['email'])
        user = self.create_user(self.user, role='P')

        obj = PatientProfile.objects.create(user=user)
        obj.full_clean()
        obj.save()

        return obj


class PatientService(UserValidationMixin):
    def __init__(self,
                 doctor_slug: str = None,
                 user: CustomUser = None,
                 mobile: str = None,
                 address: str = None,
                 appointment_date: datetime.date = None,
                 appointment_time: datetime.time = None,
                 ):
        self.mobile = mobile
        self.user = user
        self.address = address
        self.doctor_slug = doctor_slug
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time

    @transaction.atomic
    def patient_update_contact(
        self,
        slug: str
    ) -> PatientProfile:
        """Update PatientProfile instance
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


class DoctorService(UserValidationMixin):
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
        """Update DoctorProfile instance
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
        patient: PatientProfile,
    ) -> DoctorProfile:
        """Method to add patients to doctor's current list of patients
        """

        doctor: DoctorProfile = get_object(DoctorProfile, slug=slug)

        if not any(doctor_patient == patient for doctor_patient in list(doctor.patients.all())):
            doctor.patients.add(patient)
            doctor.save()
            transaction.on_commit(
                lambda: patient_add_task.delay(slug, patient.slug)
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

        if self.patients in doctor.patients.all():
            doctor.patients.remove(self.patients)
            doctor.save()

        return doctor

    @transaction.atomic
    def appointment_create(self, slug: str):
        doctor = get_object(DoctorProfile, slug=self.doctor_slug)
        patient = get_object(PatientProfile, slug=slug)
        schedule = doctor.schedulies\
            .filter(available_time__has_key=self.appointment_date)
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

                self.patient_list_update(self.doctor_slug, patient)

                transaction.on_commit(
                    lambda: consulting_appointment_task.delay(self.doctor_slug, slug)
                )

                return obj
