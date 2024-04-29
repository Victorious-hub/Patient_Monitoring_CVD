import json
from celery import shared_task

from apps.notifications.models import Notification
from django.core.serializers import serialize

from apps.users.models import DoctorProfile
from apps.users.utils import get_object


@shared_task()
def add_patient(slug: str):
    patient = DoctorProfile.objects.get(slug=slug).patients.order_by('id').last()
    doctor = get_object(DoctorProfile, slug=slug)

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
def send_appointment(slug: str) -> Notification:
    patient = DoctorProfile.objects.get(slug=slug).patients.order_by('id').last()
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
