import json
from celery import shared_task

from apps.analysis.models import BloodAnalysis, CholesterolAnalysis, Diagnosis
from .utils import predict_anomaly
from apps.notifications.models import Notification
from django.core.serializers import serialize

from apps.users.models import DoctorProfile, PatientCard, PatientProfile
from apps.users.utils import get_object


@shared_task()
def blood_analysis_notificate(slug: str, patient_slug: str):
    patient = get_object(PatientProfile, slug=patient_slug)
    doctor = get_object(DoctorProfile, slug=slug)

    notification = Notification.objects.create(
        notification_type='AN',
        patient=patient,
        message=f"Your blood analysis is ready: {doctor}",
        is_read=False,
    )

    serialized_notification = serialize('json', [notification])
    notification_data = json.loads(serialized_notification)[0]['fields']

    return notification_data


@shared_task()
def cholesterol_analysis_notificate(slug: str, patient_slug: str):
    patient = get_object(PatientProfile, slug=patient_slug)
    doctor = get_object(DoctorProfile, slug=slug)

    notification = Notification.objects.create(
        notification_type='AN',
        patient=patient,
        message=f"Your cholesterol analysis is ready: {doctor}",
        is_read=False,
    )

    serialized_notification = serialize('json', [notification])
    notification_data = json.loads(serialized_notification)[0]['fields']

    return notification_data


@shared_task()
def card_creation_notificate(slug: str, patient_slug: str):
    patient = get_object(PatientProfile, slug=patient_slug)
    doctor = get_object(DoctorProfile, slug=slug)

    notification = Notification.objects.create(
        notification_type='CD',
        patient=patient,
        message=f"Your card has been created: {doctor}",
        is_read=False,
    )
    patient.has_card = True
    patient.save()

    serialized_notification = serialize('json', [notification])
    notification_data = json.loads(serialized_notification)[0]['fields']

    return notification_data


@shared_task()
def conclusion_notificate(slug: str, patient_slug: str):
    patient = get_object(PatientProfile, slug=patient_slug)
    doctor = get_object(DoctorProfile, slug=slug)

    notification = Notification.objects.create(
        notification_type='CU',
        patient=patient,
        message=f"Conclusion: {doctor}",
        is_read=False,
    )

    serialized_notification = serialize('json', [notification])
    notification_data = json.loads(serialized_notification)[0]['fields']

    return notification_data


@shared_task()
def create_prediction(self, patient_slug: str, doctor_slug: str):
    patient_card: PatientCard = get_object(PatientCard, patient__slug=patient_slug)
    blood_obj = BloodAnalysis.objects.filter(patient=patient_card).last()
    cholesterol_obj = CholesterolAnalysis.objects.filter(patient=patient_card).last()
    doctor = get_object(DoctorProfile, slug=doctor_slug)

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
    patient_card.analysis_status = 'CT'

    print(f"Anomaly: {preditction}")

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
