import json
from celery import shared_task

from apps.notifications.models import Notification
from django.core.serializers import serialize

from apps.users.models import DoctorProfile, PatientProfile
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
def diagnosis_notificate(slug: str, patient_slug: str):
    patient = get_object(PatientProfile, slug=patient_slug)
    doctor = get_object(DoctorProfile, slug=slug)

    notification = Notification.objects.create(
        notification_type='DI',
        patient=patient,
        message=f"Diagnosis: {doctor}",
        is_read=False,
    )

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
