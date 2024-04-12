from django.contrib import admin
from .models import PatientProfile, DoctorProfile, PatientCard, CustomUser


@admin.register(CustomUser)
class CustomAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'first_name', 'last_name',
                    'role', 'is_active', 'is_staff', 'created_at', 'updated_at',
                    )
    search_fields = ('first_name', 'email',)
    list_editable = ('is_active', 'is_staff', 'first_name', 'last_name',)

    list_filter = ('email',)
    empty_value_display = "undefined"


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'weight', 'height',
                    'gender', 'age', 'birthday', 'mobile', 'slug',
                    )
    list_display_links = ('user',)
    list_editable = ('user',)

    list_filter = ('user', 'slug',)


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'patients', 'slug', 'patient_cards',)
    list_display_links = ('user',)

    list_filter = ('user', 'patients', 'slug',)


admin.site.register(PatientCard)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
