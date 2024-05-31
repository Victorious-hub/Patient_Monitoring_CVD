from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import PatientProfile


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        ANALYSIS = 'AN', _('Analysis')
        DOCTOR_LIST = 'DL', _('DoctorList')
        APPOINTMENT = 'AP', _('Appointment')
        CARD = 'CD', _('Card')
        PRESCRIPTION = 'PC', _('Prescription')
        DIAGNOSIS = 'DA', _('Diagnosis')
        CONCLUSION = 'CU', _('Conclusion')

    notification_type = models.CharField(max_length=2, choices=NotificationType.choices, default=NotificationType.ANALYSIS)
    patient = models.ForeignKey(PatientProfile, on_delete=models.PROTECT, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "notification"
        verbose_name_plural = "notifications"

    def __str__(self):
        return self.message
