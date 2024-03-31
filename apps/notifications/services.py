
from django.shortcuts import get_object_or_404
from apps.notifications.models import Notification
from apps.users.exceptions import DoctorNotFound, PatientNotFound
from apps.users.models import DoctorProfile, PatientProfile
from django.db import transaction


class NotificationService:
    def __init__(self,
                 patient: PatientProfile = None,
                 message: str = None,
                 is_read: bool = None,
                 slug: str = None,
                 ):
        self.patient = patient
        self.message = message
        self.is_read = is_read
        self.slug = slug

    @transaction.atomic
    def send_notification(self, slug):
        if not DoctorProfile.objects.filter(slug=slug).exists():
            raise DoctorNotFound

        if not PatientProfile.objects.filter(slug=self.patient.slug).exists():
            raise PatientNotFound

        obj = Notification.objects.create(
            patient=self.patient,
            message=self.message,
            is_read=self.is_read,
            doctor=get_object_or_404(DoctorProfile, slug=slug),
        )

        obj.full_clean()
        obj.save()
        return obj
