from datetime import datetime
from django.db import transaction

from .mixins import ValidationMixin

from apps.users.models import DoctorProfile, PatientProfile
from apps.users.utils import get_object

from .tasks import (
    blood_analysis_notificate,
    card_creation_notificate,
    cholesterol_analysis_notificate,
    conclusion_notificate,
    create_prediction,
)

from apps.analysis.models import (
    BloodAnalysis,
    CholesterolAnalysis,
    Conclusion,
    Diagnosis,
    PatientCard
)


class AnalysisService(ValidationMixin):
    def __init__(self,
                 weight: float = None,
                 height: int = None,
                 birthday: datetime = None,
                 gender: str = None,
                 patient: PatientProfile = None,
                 blood_analysis: BloodAnalysis = None,
                 cholesterol_analysis: CholesterolAnalysis = None,
                 anomaly: bool = False,
                 patient_slug: str = None,
                 glucose: float = None,
                 ap_hi: float = None,
                 ap_lo: float = None,
                 smoke: float = None,
                 alcohol: float = None,
                 abnormal_conditions: str = None,
                 allergies: dict = None,
                 blood_type: str = None,
                 active: float = None,
                 cholesterol: float = None,
                 hdl_cholesterol: float = None,
                 ldl_cholesterol: float = None,
                 triglycerides: float = None,
                 description: str = None,
                 recommendations: str = None,
                 ):
        self.weight = weight
        self.height = height
        self.gender = gender
        self.birthday = birthday
        self.recommendations = recommendations
        self.description = description
        self.patient = patient
        self.cholesterol_analysis = cholesterol_analysis
        self.blood_analysis = blood_analysis
        self.patient_slug = patient_slug
        self.glucose = glucose
        self.ap_hi = ap_hi
        self.ap_lo = ap_lo
        self.anomaly = anomaly
        self.smoke = smoke
        self.alcohol = alcohol
        self.abnormal_conditions = abnormal_conditions
        self.allergies = allergies
        self.blood_type = blood_type
        self.active = active
        self.cholesterol = cholesterol
        self.hdl_cholesterol = hdl_cholesterol
        self.ldl_cholesterol = ldl_cholesterol
        self.triglycerides = triglycerides

    @transaction.atomic
    def blood_analysis_create(self,
                              slug: str,
                              ) -> BloodAnalysis:
        """Method to create a blood analysis for patient
        """
        self._check_doctor_exists(slug)
        patient_card: PatientCard = get_object(PatientCard, patient__slug=self.patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        obj = BloodAnalysis.objects.create(
            patient=patient_card,
            ap_hi=self.ap_hi,
            ap_lo=self.ap_lo,
            glucose=self.glucose,
            doctor=doctor
        )
        obj.full_clean()
        obj.save()

        transaction.on_commit(
            lambda: blood_analysis_notificate.delay(slug, self.patient_slug)
        )

        if not patient_card.is_cholesterol_analysis:
            patient_card.analysis_status = 'PC'
            patient_card.is_blood_analysis = True
            patient_card.save()
        else:
            transaction.on_commit(
                lambda: create_prediction.delay(slug, self.patient_slug, slug)
            )

        return obj

    @transaction.atomic
    def chol_analysis_create(self,
                             slug: str,
                             ) -> CholesterolAnalysis:
        """Method to create a cholesterol analysis for patient
        """

        self._check_doctor_exists(slug)

        patient_card: PatientCard = get_object(PatientCard, patient__slug=self.patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        obj = CholesterolAnalysis.objects.create(
            patient=patient_card,
            cholesterol=self.cholesterol,
            hdl_cholesterol=self.hdl_cholesterol,
            ldl_cholesterol=self.ldl_cholesterol,
            triglycerides=self.triglycerides,
            doctor=doctor
        )
        obj.full_clean()
        obj.save()

        transaction.on_commit(
            lambda: cholesterol_analysis_notificate.delay(slug, self.patient_slug)
        )

        if not patient_card.is_blood_analysis:
            patient_card.analysis_status = 'PC'
            patient_card.is_cholesterol_analysis = True
            patient_card.save()
        else:
            transaction.on_commit(
                lambda: create_prediction.delay(slug, self.patient_slug, slug)
            )

        return obj

    @transaction.atomic
    def card_create(self,
                    slug: str,
                    ) -> PatientCard:
        """Function that creates patient card by doctor's slug instance
        """

        self._check_doctor_exists(slug)
        self._card_exists(self.patient)

        doctor: DoctorProfile = get_object(DoctorProfile, slug=slug)
        patient = get_object(PatientProfile, slug=self.patient_slug)

        patient_card = PatientCard.objects.create(
            abnormal_conditions=self.abnormal_conditions,
            patient=patient,
            allergies=self.allergies,
            smoke=self.smoke,
            alcohol=self.alcohol,
            blood_type=self.blood_type,
            active=self.active,
            weight=self.weight,
            height=self.height,
            gender=self.gender,
            birthday=self.birthday
        )

        patient_card.full_clean()
        patient_card.save()
        doctor.patient_cards.add(patient_card)

        transaction.on_commit(
            lambda: card_creation_notificate.delay(slug, self.patient_slug)
        )

        return patient_card

    @transaction.atomic
    def conclusion_create(self, slug) -> Conclusion:
        """Method to create a conclusion for patient
        """
        self._check_doctor_exists(slug)

        patient_card: PatientCard = get_object(PatientCard, patient__slug=self.patient_slug)
        analysis = Diagnosis.objects.filter(patient=patient_card).last()
        doctor = get_object(DoctorProfile, slug=slug)

        obj = Conclusion.objects.create(
            analysis_result=analysis,
            description=self.description,
            recommendations=self.recommendations,
            patient=patient_card,
            doctor=doctor
        )

        patient_card.analysis_status = 'NC'
        patient_card.is_blood_analysis, patient_card.is_cholesterol_analysis = False, False
        patient_card.save()

        obj.full_clean()
        obj.save()

        transaction.on_commit(
            lambda: conclusion_notificate.delay(slug, self.patient_slug)
        )

        return obj
