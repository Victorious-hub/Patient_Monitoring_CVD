from django.contrib import admin
from .models import Appointment, Medication, Prescription
from unfold.admin import ModelAdmin


@admin.register(Appointment)
class AppointmentAdmin(ModelAdmin):
    list_display = ('id', 'patient_card', 'appointment_date', 'appointment_time',
                    'created_at',
                    )
    search_fields = ('appointment_date',)
    list_display_links = ('patient_card',)
    list_filter = ('patient_card',)
    empty_value_display = "undefined"


@admin.register(Medication)
class MedicationAdmin(ModelAdmin):
    list_display = ('id', 'name', 'dosage', 'description',
                    'created_at',
                    )
    list_display_links = ('name',)
    list_editable = ('dosage', 'description', 'created_at',)
    list_filter = ('name',)
    empty_value_display = "undefined"


@admin.register(Prescription)
class PrescriptionAdmin(ModelAdmin):
    list_display = ('id', 'patient_card', 'medication',
                    'dosage', 'start_date', 'end_date',
                    )
    list_display_links = ('patient_card',)

    list_filter = ('patient_card', 'medication',)
