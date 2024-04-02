from django.db import models
from django.utils import timezone
from apps.users.models import DoctorProfile, PatientCard, PatientProfile


class Appointment(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    healthcare_provider = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.patient} with {self.healthcare_provider}"


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
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "conclusion"
        verbose_name_plural = "conclusions"

    def __str__(self):
        return f"Conclusion for {self.patient.user.first_name} on {self.date}"
