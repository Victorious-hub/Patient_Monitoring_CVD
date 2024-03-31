from django.db import transaction
from typing import Iterable
from django.db.models import Prefetch

from django.shortcuts import get_object_or_404

from apps.analysis.models import BloodAnalysis, CholesterolAnalysis, DiseaseAnalysis
from apps.users.models import DoctorProfile, PatientCard, PatientProfile


class AnalysisSelector:
    @transaction.atomic
    def list(self
             ) -> Iterable[BloodAnalysis]:
        patients = BloodAnalysis.objects.all()
        return patients

    @transaction.atomic
    def get_blood_analyses(self,
                           slug: str
                           ) -> BloodAnalysis:
        patient = get_object_or_404(PatientProfile, slug=slug)
        patient_card = get_object_or_404(PatientCard, patient=patient)
        blood_analysis = BloodAnalysis.objects.filter(patient=patient_card).order_by('id').last()

        return blood_analysis

    @transaction.atomic
    def get_cholesterol_analyses(self,
                                 slug: str
                                 ) -> CholesterolAnalysis:
        patient = get_object_or_404(PatientProfile, slug=slug)
        patient_card = get_object_or_404(PatientCard, patient=patient)
        blood_analysis = CholesterolAnalysis.objects.filter(patient=patient_card).order_by('id').last()

        return blood_analysis

    @transaction.atomic  # Optimized
    def list_disease(self, slug: str) -> DiseaseAnalysis:
        curr_doctor = get_object_or_404(DoctorProfile, slug=slug)
        patients = DiseaseAnalysis.objects.prefetch_related(
            Prefetch('patient', queryset=curr_doctor.patient_cards.all())
        )
        return patients
