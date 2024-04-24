from django.db import transaction
from typing import Iterable
from django.db.models import Prefetch

from django.shortcuts import get_object_or_404

from apps.analysis.models import BloodAnalysis, CholesterolAnalysis, Diagnosis
from apps.users.models import DoctorProfile, PatientCard, PatientProfile
from apps.users.utils import get_object


class AnalysisSelector:
    @transaction.atomic
    def blood_analysis_list(self
                            ) -> Iterable[BloodAnalysis]:
        patients = BloodAnalysis.objects.all()
        return patients

    @transaction.atomic
    def blood_analysis_get(self,
                           slug: str
                           ) -> BloodAnalysis:
        patient = get_object(PatientProfile, slug=slug)
        patient_card = get_object(PatientCard, patient=patient)
        blood_analysis = BloodAnalysis.objects.filter(patient=patient_card)
        # blood_analysis = BloodAnalysis.objects.filter(patient=patient_card).order_by('id').last()

        return blood_analysis

    @transaction.atomic
    def cholesterol_analysis_get(self,
                                 slug: str
                                 ) -> CholesterolAnalysis:
        patient = get_object(PatientProfile, slug=slug)
        patient_card = get_object(PatientCard, patient=patient)
        cholesterol_analysis = CholesterolAnalysis.objects.filter(patient=patient_card)
        # blood_analysis = CholesterolAnalysis.objects.filter(patient=patient_card).order_by('id').last()

        return cholesterol_analysis

    @transaction.atomic  # Optimized
    def diagnosis_list(self, slug: str) -> Diagnosis:
        curr_doctor = get_object(DoctorProfile, slug=slug)
        patients = Diagnosis.objects.prefetch_related(
            Prefetch('patient', queryset=curr_doctor.patient_cards.all())
        )
        return patients

    @transaction.atomic
    def card_list(self) -> Iterable[PatientCard]:
        cards = PatientCard.objects.all()
        return cards

    @transaction.atomic
    def patient_get_card(self, slug: str) -> PatientCard:
        patient = get_object_or_404(PatientProfile, slug=slug)

        patient_card = PatientCard.objects.get(patient=patient)
        return patient_card
