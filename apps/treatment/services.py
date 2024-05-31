import datetime
import time
from django.db import transaction

from apps.analysis.mixins import ValidationMixin
from apps.treatment.models import Appointment, Medication, Prescription
from apps.users.models import DoctorProfile
from apps.users.tasks import appointment_patient_task
from apps.users.utils import get_object

from apps.treatment.tasks import (
    prescription_decline_notification_task,
    prescription_patient_task
)


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
    def create_medication(self) -> Medication:
        """Create Medication instance objects
        """
        obj = Medication.objects.create(
            name=self.name,
            dosage=self.dosage,
            description=self.description,
            created_at=self.created_at,
        )

        obj.full_clean()
        obj.save()

        return obj


class TreatmentService(ValidationMixin):
    def __init__(self,
                 id: int = None,
                 patient_slug: str = None,
                 medication: Medication = None,
                 dosage: str = None,
                 start_date: datetime = None,
                 end_date: datetime = None,
                 appointment_date: datetime = None,
                 appointment_time: time = None,
                 text: str = None,
                 ):
        self.patient_slug = patient_slug
        self.medication = medication
        self.dosage = dosage
        self.start_date = start_date
        self.end_date = end_date
        self.text = text
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.id = id

    @transaction.atomic
    def prescription_create(
        self,
        slug: str,
    ) -> Medication:
        """Create Prescription instance objects
        """

        self._check_doctor_exists(slug)

        doctor = get_object(DoctorProfile, slug=slug)
        patient_card = doctor.patient_cards.get(patient__slug=self.patient_slug)

        obj = Prescription.objects.create(
            patient_card=patient_card,
            medication=self.medication,
            dosage=self.dosage,
            start_date=self.start_date,
            end_date=self.end_date,
            doctor=doctor,
        )

        obj.full_clean()
        obj.save()

        transaction.on_commit(
            lambda: prescription_patient_task.delay(slug, self.patient_slug)
        )

        return obj

    @transaction.atomic
    def appointment_create(
        self,
        slug: str
    ) -> Appointment:
        """Method to place an appointment for patient
        """
        self._check_doctor_exists(slug)

        doctor = get_object(DoctorProfile, slug=slug)
        patient = doctor.patients.get(slug=self.patient_slug)

        obj = Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=self.appointment_date,
            appointment_time=self.appointment_time
        )

        obj.full_clean()
        obj.save()

        transaction.on_commit(
            lambda: appointment_patient_task.delay(slug, self.patient_slug)
        )

        return obj

    @transaction.atomic
    def prescription_decline(self, slug: str):
        self._check_doctor_exists(slug)

        prescription = get_object(Prescription, id=self.id)
        prescription.is_declined = True
        prescription.save()
        transaction.on_commit(
            lambda: prescription_decline_notification_task.delay(prescription.id, self.patient_slug)
        )

        return prescription
