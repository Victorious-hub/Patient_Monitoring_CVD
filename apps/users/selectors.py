from typing import Iterable
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from apps.users.models import (
    DoctorProfile,
    PatientCard,
    PatientProfile
)


class PatientSelector:
    @transaction.atomic
    def list(self) -> Iterable[PatientProfile]:
        patients = PatientProfile.objects.all()
        return patients

    @transaction.atomic
    def get(self, slug: str) -> PatientProfile:
        patient = get_object_or_404(PatientProfile, slug=slug)
        return patient

    @transaction.atomic
    def get_card(self, slug: str) -> PatientCard:
        patient = get_object_or_404(PatientProfile, slug=slug)

        patient_card = PatientCard.objects.get(patient=patient)
        return patient_card


class DoctorSelector:
    @transaction.atomic
    def list(self) -> Iterable[DoctorProfile]:
        doctors = DoctorProfile.objects.all()
        return doctors

    @transaction.atomic
    def get(self, slug: str) -> PatientProfile:
        doctor = DoctorProfile.objects.select_related('user').prefetch_related(
            Prefetch('patient_cards', queryset=PatientCard.objects.all()),
            Prefetch('patients', queryset=PatientProfile.objects.all())
        )
        doctor = doctor.get(slug=slug)
        return doctor

    @transaction.atomic
    def card_list(self) -> Iterable[PatientCard]:
        cards = PatientCard.objects.all()
        return cards
