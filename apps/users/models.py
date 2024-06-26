from datetime import date
from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class RoleType(models.TextChoices):
        PATIENT = 'P', _('Patient')
        DOCTOR = 'D', _('Doctor')

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=255, choices=RoleType.choices, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return f"Custom User: {self.first_name} - {self.last_name}"


class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    has_card = models.BooleanField(default=False, blank=True, null=True)
    mobile = models.CharField(max_length=11, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True, editable=False)

    class Meta:
        verbose_name = "patient"
        verbose_name_plural = "patients"

    def __str__(self):
        return f"Patient: {self.user.first_name} - {self.user.last_name}"

    def save(self, *args, **kwargs):
        slug_data = self.user.email.split('@')[0]
        self.slug = slugify(slug_data)
        return super(PatientProfile, self).save(*args, **kwargs)


class PatientCard(models.Model):
    class BloodType(models.TextChoices):
        GROUP_1 = 'Group I', _('I')
        GROUP_2 = 'Group II', _('II')
        GROUP_3 = 'Group III', _('III')
        GROUP_4 = 'Group IV', _('IV')

    class GenderType(models.TextChoices):
        MALE = 'Male', _('Male')
        FEMALE = 'Female', _('Female')
        NONE = 'None', _('None')

    patient = models.OneToOneField(PatientProfile, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=255, choices=BloodType.choices)
    allergies = models.JSONField(default=list, null=True, blank=True)
    abnormal_conditions = models.TextField()
    smoke = models.BooleanField()
    alcohol = models.BooleanField()
    active = models.BooleanField()
    weight = models.FloatField(blank=True, null=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(300)
    ])
    height = models.IntegerField(blank=True, null=True, validators=[
        MinValueValidator(1),
        MaxValueValidator(220)
    ])
    gender = models.CharField(blank=True, null=True, max_length=255, choices=GenderType.choices, default="None")
    age = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    is_cholesterol_analysis = models.BooleanField(default=False)
    is_blood_analysis = models.BooleanField(default=False)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Patient Card: {self.patient.user.first_name} - {self.patient.user.last_name}"

    class Meta:
        verbose_name = "card"
        verbose_name_plural = "cards"

    def save(self, *args, **kwargs):
        if self.birthday:
            delta = date.today() - self.birthday
            self.age = delta.days // 365
        super().save(*args, **kwargs)


class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    patients = models.ManyToManyField(PatientProfile, related_name='patients')
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True, editable=False)
    patient_cards = models.ManyToManyField(PatientCard, related_name='patient_cards')
    profile_image = models.ImageField(upload_to='images/', null=False, blank=True, default='images/account.png')
    description = models.TextField(default="")
    experience = models.IntegerField(default=0)

    class Meta:
        verbose_name = "doctor"
        verbose_name_plural = "doctors"

    def __str__(self):
        return f"Doctor: {self.user.first_name} - {self.user.last_name}"

    def save(self, *args, **kwargs):
        slug_data = self.user.email.split('@')[0]
        self.slug = slugify(slug_data)
        return super(DoctorProfile, self).save(*args, **kwargs)


class Schedule(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='schedulies')
    available_time = models.JSONField()

    class Meta:
        verbose_name = "schedule"
        verbose_name_plural = "schedulies"

    def __str__(self):
        return f"Doctor: {self.doctor}"
