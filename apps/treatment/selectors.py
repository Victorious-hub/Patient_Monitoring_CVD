
from typing import Iterable
from django.db import transaction
from apps.treatment.models import Medication, Prescription


class MedicationSelector:

    @transaction.atomic
    def medication_list(self) -> Iterable[Medication]:
        medications = Medication.objects.all()
        return medications


class PrescriptionSelector:

    @transaction.atomic
    def prescription_list(self) -> Iterable[Prescription]:
        prescriptions = Prescription.objects.all()
        return prescriptions

    # @transaction.atomic
    # def patient_prescription_list(self,
    #                             slug: str
    #                             ) -> Iterable[Prescription]:

    #     patient = get_object_or_404(PatientProfile, slug=slug)
    #     patient_card = PatientCard.objects.get(patient=patient)
    #     prescriptions = get_object_or_404(Prescription, patient_card=slug)
    #     return prescriptions
