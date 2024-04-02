import datetime
import time
from django.db import transaction

from apps.treatment.models import Appointment, Conclusion, Medication, Prescription
from apps.users.exceptions import DoctorNotFound
from apps.users.models import DoctorProfile, PatientCard


class MedicationService:
    def __init__(self,
                 name: str = None,
                 dosage: str = None,
                 description: str = None,
                 created_at: datetime = None,
                 ):
        self.name = name
        self.dosage = dosage
        self.description = description
        self.created_at = created_at

    @transaction.atomic
    def create(self) -> Medication:

        obj = Medication.objects.create(
            name=self.name,
            dosage=self.dosage,
            description=self.description,
            created_at=self.created_at,
        )

        obj.full_clean()
        obj.save()

        return obj


class PrescriptionService:
    def __init__(self,
                 patient_card: PatientCard = None,
                 medication: Medication = None,
                 dosage: str = None,
                 start_date: datetime = None,
                 end_date: datetime = None,
                 ):
        self.patient_card = patient_card
        print(self.patient_card)
        self.medication = medication
        self.dosage = dosage
        self.start_date = start_date
        self.end_date = end_date

    @transaction.atomic
    def create(self,
               slug: str,
               ) -> Medication:

        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

        obj = Prescription.objects.create(
            patient_card=self.patient_card,
            medication=self.medication,
            dosage=self.dosage,
            start_date=self.start_date,
            end_date=self.end_date,
        )

        obj.full_clean()
        obj.save()

        return obj


class AppointmentService:
    def __init__(self,
                 patient_card: PatientCard = None,
                 appointment_date: datetime = None,
                 appointment_time: time = None,
                 text: str = None,
                 ):
        self.patient_card = patient_card
        self.text = text
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time

    @transaction.atomic
    def create_appointment(self, slug) -> Conclusion:
        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

        obj = Appointment.objects.create(
            patient_card=self.patient_card,
            appointment_date=self.appointment_date,
            appointment_time=self.appointment_time
        )

        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def create_conclusion(self, slug) -> Conclusion:
        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

        obj = Conclusion.objects.create(
            patient_card=self.patient_card,
            text=self.text,
        )

        obj.full_clean()
        obj.save()

        return obj
