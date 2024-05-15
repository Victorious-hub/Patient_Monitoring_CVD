from django.db import models
from nbformat import ValidationError
from apps.users.models import DoctorProfile, PatientCard, PatientProfile


class Appointment(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.DO_NOTHING)
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    appointment_date = models.DateField(blank=True, null=True)
    appointment_time = models.TimeField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.patient} from {self.doctor}"


class Medication(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dosage = models.FloatField(default=0)
    description = models.TextField()
    created_at = models.DateField()

    class Meta:
        verbose_name = "medication"
        verbose_name_plural = "medications"

    def __str__(self):
        return f"Medication: {self.name}"


class Prescription(models.Model):
    patient_card = models.ForeignKey(PatientCard, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        verbose_name = "prescription"
        verbose_name_plural = "prescriptions"

    def __str__(self):
        return f"Prescription for {self.patient_card} - {self.medication}"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("End date cannot be before start date")
