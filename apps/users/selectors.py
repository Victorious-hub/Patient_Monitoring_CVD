from typing import Iterable
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404

from apps.users.models import (
    DoctorProfile,
    PatientCard,
    PatientProfile,
    Schedule
)
from apps.users.utils import get_object


class PatientSelector:
    @transaction.atomic
    def patient_list(self) -> Iterable[PatientProfile]:
        patients = PatientProfile.objects.all()
        return patients

    @transaction.atomic
    def patient_get(self, slug: str) -> PatientProfile:
        patient = get_object_or_404(PatientProfile, slug=slug)
        return patient

    @transaction.atomic
    def patient_doctor_list(self, slug: str) -> PatientProfile:
        patient = get_object_or_404(PatientProfile, slug=slug)
        doctors = DoctorProfile.objects.filter(patients=patient).all()
        return doctors


class DoctorSelector:
    @transaction.atomic
    def doctor_list(self) -> Iterable[DoctorProfile]:
        doctors = DoctorProfile.objects.all()
        return doctors

    @transaction.atomic
    def doctor_get(self, slug: str) -> DoctorProfile:
        doctor = DoctorProfile.objects.select_related('user').prefetch_related(
            Prefetch('patient_cards', queryset=PatientCard.objects.all()),
            Prefetch('patients', queryset=PatientProfile.objects.all())
        )
        doctor = doctor.get(slug=slug)
        return doctor

    @transaction.atomic
    def doctor_get_patients(self, slug: str) -> Iterable[PatientProfile]:
        doctor = DoctorProfile.objects.select_related('user').prefetch_related(
            Prefetch('patient_cards', queryset=PatientCard.objects.all()),
            Prefetch('patients', queryset=PatientProfile.objects.all())
        )
        doctor = doctor.get(slug=slug)
        return doctor

    @transaction.atomic
    def schedule_list(self) -> Iterable[Schedule]:
        schedule = Schedule.objects.all()
        return schedule

    @transaction.atomic
    def schedule_detail(self, slug) -> Iterable[Schedule]:
        doctor = get_object(DoctorProfile, slug=slug)
        doctor_schedule = get_object(Schedule, doctor=doctor)
        return doctor_schedule
