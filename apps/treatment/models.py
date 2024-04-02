from django.db import models
from django.utils import timezone
from apps.users.models import PatientCard


class Appointment(models.Model):
    patient_card = models.ForeignKey(PatientCard, on_delete=models.CASCADE)
    appointment_date = models.DateField(blank=True, null=True)
    appointment_time = models.TimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Appointment for {self.patient_card}"


class Medication(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dosage = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField()

    class Meta:
        verbose_name = "medication"
        verbose_name_plural = "medications"

    def __str__(self):
        return self.name


class Prescription(models.Model):
    patient_card = models.ForeignKey(PatientCard, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "prescription"
        verbose_name_plural = "prescriptions"

    def __str__(self):
        return f"Prescription for {self.patient_card} - {self.medication}"


class Conclusion(models.Model):
    patient_card = models.ForeignKey(PatientCard, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "prescription"
        verbose_name_plural = "prescriptions"

    def __str__(self):
        return f"Prescription for {self.patient_card}"
