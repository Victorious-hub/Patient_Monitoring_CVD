from django.contrib import admin
from .models import Appointment, Medication, Prescription


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_card', 'appointment_date', 'appointment_time',
                    'created_at',
                    )
    search_fields = ('appointment_date',)
    list_display_links = ('patient_card',)
    list_filter = ('patient_card',)
    empty_value_display = "undefined"


@admin.register(Medication)
class MedicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'dosage', 'description',
                    'created_at',
                    )
    list_display_links = ('name',)
    list_editable = ('dosage', 'description', 'created_at',)
    list_filter = ('name',)
    empty_value_display = "undefined"


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_card', 'medication',
                    'dosage', 'start_date', 'end_date',
                    )
    list_display_links = ('patient_card',)

    list_filter = ('patient_card', 'medication',)
