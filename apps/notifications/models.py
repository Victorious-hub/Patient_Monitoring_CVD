from django.utils import timezone
from django.db import models

from apps.users.models import DoctorProfile, PatientProfile


class Notification(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name='patients_notification')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='doctors_notification')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date_sent = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "notification"
        verbose_name_plural = "notifications"

    def __str__(self):
        return self.message
