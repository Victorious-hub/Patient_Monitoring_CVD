import os
import pickle
from django.db import transaction
import numpy as np

from .mixins import ValidationMixin

from apps.users.models import DoctorProfile, PatientProfile
from apps.users.utils import get_object

from .tasks import (
    blood_analysis_notificate,
    card_creation_notificate,
    cholesterol_analysis_notificate,
    conclusion_notificate,
    diagnosis_notificate
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
                 patient: PatientProfile = None,
                 blood_analysis: BloodAnalysis = None,
                 cholesterol_analysis: CholesterolAnalysis = None,
                 anomaly: bool = False,
                 patient_card: PatientCard = None,
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
        self.recommendations = recommendations
        self.description = description
        self.patient = patient
        self.cholesterol_analysis = cholesterol_analysis,
        self.blood_analysis = blood_analysis,
        self.patient_card = patient_card
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

    def _predict_anomaly(self, features: list):
        model_path = os.path.join(os.path.dirname(__file__), 'model', 'anomaly_prediction.pkl')
        with open(model_path, 'rb') as file:
            model = pickle.load(file)

        new_data = np.array(list(features)).reshape(1, -1)
        predicted_anomaly = model.predict(new_data)[0]
        return predicted_anomaly

    @transaction.atomic
    def blood_analysis_create(self,
                              slug: str,
                              ) -> BloodAnalysis:
        """Method to create a blood analysis for patient
        """

        self._check_doctor_exists(slug)
        patient_card = get_object(PatientCard, patient=self.patient_card.patient)

        obj = BloodAnalysis.objects.create(
            patient=patient_card,
            ap_hi=self.ap_hi,
            ap_lo=self.ap_lo,
            glucose=self.glucose,
        )
        obj.full_clean()
        obj.save()

        transaction.on_commit(
            lambda: blood_analysis_notificate.delay(slug, self.patient_card.patient.slug)
        )

        return obj

    @transaction.atomic
    def chol_analysis_create(self,
                             slug: str,
                             ) -> CholesterolAnalysis:
        """Method to create a cholesterol analysis for patient
        """

        self._check_doctor_exists(slug)

        patient_card = get_object(PatientCard, patient=self.patient_card.patient)

        obj = CholesterolAnalysis.objects.create(
            patient=patient_card,
            cholesterol=self.cholesterol,
            hdl_cholesterol=self.hdl_cholesterol,
            ldl_cholesterol=self.ldl_cholesterol,
            triglycerides=self.triglycerides
        )
        obj.full_clean()
        obj.save()

        transaction.on_commit(
            lambda: cholesterol_analysis_notificate.delay(slug, self.patient_card.patient.slug)
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

        patient_card = PatientCard.objects.create(
            abnormal_conditions=self.abnormal_conditions,
            patient=self.patient,
            allergies=self.allergies,
            smoke=self.smoke,
            alcohol=self.alcohol,
            blood_type=self.blood_type,
            active=self.active
        )

        patient_card.full_clean()
        patient_card.save()
        doctor.patient_cards.add(patient_card)

        transaction.on_commit(
            lambda: card_creation_notificate.delay(slug, self.patient.slug)
        )

        return patient_card

    @transaction.atomic
    def diagnosis_create(
        self,
        slug: str,
    ) -> Diagnosis:
        """Method to predict a potential cvd anomalies for patient
        """

        self._check_doctor_exists(slug)

        patient_card: PatientCard = get_object(PatientCard, patient=self.patient_card.patient)
        blood_obj = BloodAnalysis.objects.filter(patient=patient_card).last()
        cholesterol_obj = CholesterolAnalysis.objects.filter(patient=patient_card).last()

        patient_card.patient.gender = 1 if patient_card.patient.gender == "Male" else 0
        preditction = self._predict_anomaly([
            blood_obj.ap_hi,
            blood_obj.ap_lo,
            blood_obj.glucose,
            cholesterol_obj.cholesterol,
            patient_card.active,
            patient_card.alcohol,
            patient_card.smoke,
            patient_card.patient.age,
            patient_card.patient.gender,
            patient_card.patient.height,
            patient_card.patient.weight,
        ])

        print(f"Anomaly: {preditction}")

        obj = Diagnosis.objects.create(
            patient=patient_card,
            blood_analysis=blood_obj,
            cholesterol_analysis=cholesterol_obj,
            anomaly=preditction,
        )
        obj.full_clean()
        obj.save()

        transaction.on_commit(
            lambda: diagnosis_notificate.delay(slug, self.patient_card.patient.slug)
        )

        return obj

    @transaction.atomic
    def conclusion_create(self, slug) -> Conclusion:
        """Method to create a conclusion for patient
        """
        self._check_doctor_exists(slug)

        patient_card = get_object(PatientCard, patient=self.patient_card.patient)
        analysis = get_object(Diagnosis, patient_card=patient_card)

        obj = Conclusion.objects.create(
            analysis_result=analysis,
            description=self.description,
            recommendations=self.recommendations,
        )

        obj.full_clean()
        obj.save()

        transaction.on_commit(
            lambda: conclusion_notificate.delay(slug, self.patient_card.patient.slug)
        )

        return obj
