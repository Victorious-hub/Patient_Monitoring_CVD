import json
from celery import shared_task

from apps.notifications.models import Notification
from django.core.serializers import serialize

from apps.users.models import DoctorProfile, PatientProfile
from apps.users.utils import get_object


@shared_task()
def add_patient(slug: str, patient_slug: str):
    patient = get_object(PatientProfile, slug=patient_slug)
    doctor = get_object(DoctorProfile, slug=slug)
    print(patient)
    notification = Notification.objects.create(
        notification_type='DL',
        patient=patient,
        message=f"You were added to {doctor} list",
        is_read=False,
    )

    serialized_notification = serialize('json', [notification])
    notification_data = json.loads(serialized_notification)[0]['fields']

    return notification_data


@shared_task()
def send_appointment(slug: str, patient_slug: str) -> Notification:
    patient = get_object(PatientProfile, slug=patient_slug)
    doctor = get_object(DoctorProfile, slug=slug)

    notification = Notification.objects.create(
        notification_type='AP',
        patient=patient,
        message=f"Doctor {doctor} has indidcated an appointment for you",
        is_read=False,
    )

    serialized_notification = serialize('json', [notification])
    notification_data = json.loads(serialized_notification)[0]['fields']

    return notification_data
