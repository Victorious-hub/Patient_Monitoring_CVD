
from celery import shared_task

from apps.analysis.utils import send_notification
from apps.notifications.models import Notification
from apps.treatment.models import Prescription
from apps.users.models import DoctorProfile, PatientProfile
from apps.users.utils import get_object


@shared_task
def prescription_decline_notification_task(
        prescription_id: Prescription,
        patient_slug: PatientProfile
) -> Notification:
    try:
        prescription = get_object(Prescription, id=prescription_id)
        patient = get_object(PatientProfile, slug=patient_slug)

        notification_type = 'PC',
        message = f"Prescription {prescription} has been decliend",
        send_notification(notification_type, message, patient)
    except Exception:
        pass


@shared_task
def prescription_patient_task(slug: str, patient_slug: str) -> Notification:
    try:
        patient = get_object(PatientProfile, slug=patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        notification_type = 'PC',
        message = f"Your prescription has been created: {doctor}",
        send_notification(notification_type, message, patient)
    except Exception:
        pass
