from django.db import models

from apps.users.models import PatientCard, PatientProfile


class Medication(models.Model):
    name = models.CharField(max_length=100, unique=True)
    dosage = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.name


class Prescription(models.Model):
    patient_card = models.ForeignKey(PatientCard, on_delete=models.CASCADE)
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.patient_card} - {self.medication}"


class Conclusion(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    conclusion_text = models.TextField()
    date12 = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Conclusion for {self.patient.user.first_name} on {self.date}"
