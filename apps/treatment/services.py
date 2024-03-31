import datetime
from django.db import transaction

from apps.treatment.models import Medication, Prescription
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
