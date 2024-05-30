from celery import shared_task

from apps.analysis.models import BloodAnalysis, CholesterolAnalysis, Diagnosis
from .utils import predict_anomaly, send_notification

from apps.users.models import DoctorProfile, PatientCard, PatientProfile
from apps.users.utils import get_object


@shared_task
def blood_analysis_notification_task(slug: str, patient_slug: str):
    try:
        patient = get_object(PatientProfile, slug=patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        notification_type = 'AN'
        message = f"Your blood analysis is ready: {doctor}"
        send_notification(notification_type, message, patient)
    except Exception:
        pass


@shared_task
def cholesterol_analysis_notification_task(slug: str, patient_slug: str):
    try:
        patient = get_object(PatientProfile, slug=patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        notification_type = 'AN'
        message = f"Your cholesterol analysis is ready: {doctor}"
        send_notification(notification_type, message, patient)
    except Exception:
        pass


@shared_task
def card_create_notification_task(slug: str, patient_slug: str):
    try:
        patient = get_object(PatientProfile, slug=patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        notification_type = 'CD'
        message = f"Your card has been created: {doctor}"
        send_notification(notification_type, message, patient)
        patient.has_card = True
        patient.save()
    except Exception:
        pass


@shared_task
def conclusion_notification_task(slug: str, patient_slug: str):
    try:
        patient = get_object(PatientProfile, slug=patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        notification_type = 'CU',
        message = f"Your conclusion has been created: {doctor}"
        send_notification(notification_type, message, patient)
    except Exception:
        pass


@shared_task
def prediction_create_task(patient_slug: str, doctor_slug: str):
    try:
        patient_card: PatientCard = get_object(PatientCard, patient__slug=patient_slug)
        blood_obj = BloodAnalysis.objects.filter(patient=patient_card).last()
        cholesterol_obj = CholesterolAnalysis.objects.filter(patient=patient_card).last()
        doctor: DoctorProfile = get_object(DoctorProfile, slug=doctor_slug)

        patient_card.gender = 1 if patient_card.gender == "Male" else 0
        preditction = predict_anomaly([
            blood_obj.ap_hi,
            blood_obj.ap_lo,
            blood_obj.glucose,
            cholesterol_obj.cholesterol,
            patient_card.active,
            patient_card.alcohol,
            patient_card.smoke,
            patient_card.age,
            patient_card.gender,
            patient_card.height,
            patient_card.weight,
        ])
        patient_card.is_cholesterol_analysis = True
        patient_card.is_blood_analysis = True

        obj = Diagnosis.objects.create(
            patient=patient_card,
            blood_analysis=blood_obj,
            cholesterol_analysis=cholesterol_obj,
            anomaly=preditction,
            doctor=doctor
        )

        obj.full_clean()
        obj.save()
        patient_card.save()
    except Exception:
        pass
