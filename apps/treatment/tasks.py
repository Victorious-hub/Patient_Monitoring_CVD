
from celery import shared_task

from apps.analysis.utils import send_notification
from apps.treatment.models import Prescription
from apps.users.models import PatientProfile
from apps.users.utils import get_object


@shared_task
def prescription_decline_notification_task(prescription_id: Prescription, patient_slug: PatientProfile):
    try:
        prescription = Prescription.objects.get(id=prescription_id)
        patient = get_object(PatientProfile, slug=patient_slug)

        notification_type = 'PC',
        message = f"Prescription {prescription} has been decliend",
        send_notification(notification_type, message, patient)
    except Exception:
        pass
