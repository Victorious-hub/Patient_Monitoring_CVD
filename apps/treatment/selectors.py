
from typing import Iterable
from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.treatment.models import Appointment, Medication, Prescription
from apps.users.models import PatientCard, PatientProfile


class TreatmentSelector:

    @transaction.atomic
    def prescription_list(self) -> Iterable[Prescription]:
        prescriptions = Prescription.objects.all()
        return prescriptions

    @transaction.atomic
    def patient_prescription_list(self, slug: str) -> Iterable[Prescription]:
        patient = get_object_or_404(PatientProfile, slug=slug)
        patient_card = PatientCard.objects.get(patient=patient)
        prescriptions = Prescription.objects.filter(patient_card=patient_card)
        return prescriptions

    @transaction.atomic
    def medication_list(self) -> Iterable[Medication]:
        medications = Medication.objects.all()
        return medications

    @transaction.atomic
    def doctor_appointment_list(self, slug) -> Iterable[Appointment]:
        appointments = Appointment.objects.filter(doctor__slug=slug)
        return appointments

    @transaction.atomic
    def patient_appointment_list(self, slug) -> Iterable[Appointment]:
        appointments = Appointment.objects.filter(patient__slug=slug)
        return appointments

    @transaction.atomic
    def doctor_prescription_list(self, slug: str) -> Iterable[Prescription]:
        prescriptions = Prescription.objects.filter(doctor__slug=slug)
        return prescriptions
