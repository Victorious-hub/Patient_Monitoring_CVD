from datetime import datetime, date
from celery import shared_task

from apps.analysis.utils import send_notification
from apps.notifications.models import Notification

from apps.users.models import DoctorProfile, PatientProfile, Schedule
from apps.users.utils import get_object


@shared_task
def patient_add_task(slug: str, patient_slug: str) -> Notification:
    try:
        patient = get_object(PatientProfile, slug=patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        notification_type = 'DL'
        message = f"You were added to {doctor} list"
        send_notification(notification_type, message, patient)
    except Exception:
        pass


@shared_task
def appointment_patient_task(slug: str, patient_slug: str) -> Notification:
    try:
        patient = get_object(PatientProfile, slug=patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        notification_type = 'AP',
        message = f"Doctor {doctor} has indidcated an appointment for you",
        send_notification(notification_type, message, patient)
    except Exception:
        pass


@shared_task
def consulting_appointment_task(slug: str, patient_slug: str) -> Notification:
    try:
        patient = get_object(PatientProfile, slug=patient_slug)
        doctor = get_object(DoctorProfile, slug=slug)

        notification_type = 'AP',
        message = f"You have been appointed to doctor: {doctor}",
        send_notification(notification_type, message, patient)
    except Exception:
        pass


@shared_task
def filter_schedule_task():
    try:
        schedule = Schedule.objects.all()
        if schedule:
            for key, _ in schedule.available_time.items():
                if datetime.strptime(key, '%Y-%m-%d').date() < date.today():
                    del schedule.available_time[datetime.strptime(key, '%Y-%m-%d').date()]
            schedule.save()
    except Exception:
        pass
