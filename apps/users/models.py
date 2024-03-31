from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from apps.users.constansts import (
    BLOOD_TYPE,
    GENDER,
    ROLES,
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient')
    weight = models.FloatField(blank=True, null=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(300)
    ])
    height = models.IntegerField(blank=True, null=True)
    gender = models.CharField(blank=True, null=True, max_length=255, choices=GENDER, default="None")
    age = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    role = models.CharField(max_length=255, choices=ROLES, default='P', blank=True, null=True)
    mobile = models.CharField(max_length=11, unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = "patient"
        verbose_name_plural = "patients"

    def __str__(self):
        return f"Patient: {self.user.first_name}"

    def save(self, *args, **kwargs):
        slug_data = self.user.email.split('@')[0]
        self.slug = slugify(slug_data)
        return super(PatientProfile, self).save(*args, **kwargs)


class PatientCard(models.Model):
    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE, related_name='patient_card')
    blood_type = models.CharField(max_length=255, choices=BLOOD_TYPE)
    allergies = models.JSONField(default=list)
    abnormal_conditions = models.TextField()
    smoke = models.BooleanField()
    alcohol = models.BooleanField()
    active = models.BooleanField()

    def __str__(self):
        return self.patient.user.first_name

    class Meta:
        verbose_name = "card"
        verbose_name_plural = "cards"


class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    patients = models.ManyToManyField(PatientProfile, related_name='patients')
    role = models.CharField(max_length=255, choices=ROLES, default='D', null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True, editable=False)
    patient_cards = models.ManyToManyField(PatientCard, related_name='patient_cards')

    class Meta:
        verbose_name = "doctor"
        verbose_name_plural = "doctors"

    def __str__(self):
        return self.user.first_name

    def save(self, *args, **kwargs):
        slug_data = self.user.email.split('@')[0]
        self.slug = slugify(slug_data)
        return super(DoctorProfile, self).save(*args, **kwargs)
