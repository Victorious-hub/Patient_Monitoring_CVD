from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.analysis.models import BloodAnalysis, CholesterolAnalysis, DiseaseAnalysis, PatientCard
from apps.analysis.tasks import predict_anomaly
from apps.users.exceptions import DoctorNotFound, PatientCardExists, PatientNotFound
from apps.users.models import DoctorProfile, PatientProfile


class CardService:
    def __init__(self,
                 patient: PatientProfile = None,
                 blood_type: str = None,
                 allergies: dict = None,
                 abnormal_conditions: str = None,
                 smoke: bool = None,
                 alcohol: bool = None,
                 active: bool = None
                 ):
        self.patient = patient
        self.blood_type = blood_type
        self.allergies = allergies
        self.abnormal_conditions = abnormal_conditions
        self.smoke = smoke
        self.alcohol = alcohol
        self.active = active

    @transaction.atomic
    def card_create(self,
                    slug: str,
                    ) -> PatientCard:
        """Function that creates patient card by doctor's slug instance
        """

        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

        if PatientCard.objects.filter(patient=self.patient).exists():
            raise PatientCardExists

        doctor = get_object_or_404(DoctorProfile, slug=slug)
        print(self.patient)
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

        return patient_card


class AnalysisService:
    def __init__(self,
                 blood_analysis: BloodAnalysis = None,
                 cholesterol_analysis: CholesterolAnalysis = None,
                 anomaly: bool = False,
                 patient_card: int = None,
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
                 patient: int = None,
                 ):
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
        self.patient = patient,

    @transaction.atomic
    def create_blood_analysis(self,
                              slug: str,
                              ) -> BloodAnalysis:

        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

        patient_card = PatientCard.objects.get(patient=self.patient_card.patient)

        obj = BloodAnalysis.objects.create(
            patient=patient_card,
            ap_hi=self.ap_hi,
            ap_lo=self.ap_lo,
            glucose=self.glucose,
        )
        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def create_cholesterol_analysis(self,
                                    slug: str,
                                    ) -> CholesterolAnalysis:

        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

        patient_card = PatientCard.objects.get(patient=self.patient_card.patient)

        obj = CholesterolAnalysis.objects.create(
            patient=patient_card,
            cholesterol=self.cholesterol,
            hdl_cholesterol=self.hdl_cholesterol,
            ldl_cholesterol=self.ldl_cholesterol,
            triglycerides=self.triglycerides
        )
        obj.full_clean()
        obj.save()

        return obj

    @transaction.atomic
    def card_create(self,
                    slug: str,
                    ) -> PatientCard:

        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

        if not PatientProfile.objects.filter(id=self.patient).exists():
            raise PatientNotFound

        if PatientCard.objects.filter(patient=self.patient).exists():
            raise PatientCardExists

        curr_patient = PatientProfile.objects.get(id=self.patient)
        doctor = get_object_or_404(DoctorProfile, slug=slug)

        patient_card = PatientCard.objects.create(
            abnormal_conditions=self.abnormal_conditions,
            patient=curr_patient,
            allergies=self.allergies,
            smoke=self.smoke,
            alcohol=self.alcohol,
            blood_type=self.blood_type,
            active=self.active
        )

        patient_card.full_clean()
        patient_card.save()
        doctor.patient_cards.add(patient_card)

        return patient_card

    @transaction.atomic
    def create_disease_prediction(self,
                                  slug: str,
                                  ) -> DiseaseAnalysis:

        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

        patient_card = PatientCard.objects.get(patient=self.patient_card.patient)
        blood_obj = BloodAnalysis.objects.filter(patient=patient_card).last()
        cholesterol_obj = CholesterolAnalysis.objects.filter(patient=patient_card).order_by('id').last()
        print(patient_card)
        patient_card.patient.gender = 1
        preditction = predict_anomaly([
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

        obj = DiseaseAnalysis.objects.create(
            patient=patient_card,
            blood_analysis=blood_obj,
            cholesterol_analysis=cholesterol_obj,
            anomaly=preditction,
        )
        obj.full_clean()
        obj.save()

        return obj
