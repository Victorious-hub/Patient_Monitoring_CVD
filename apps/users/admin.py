from django.contrib import admin
from .models import PatientProfile, DoctorProfile, PatientCard, CustomUser


# class CustomAccountAdmin(admin.ModelAdmin):
#     list_display = ('id', 'email', 'first_name', 'slug', 'last_name', 'mobile', 'gender',
#                     'role', 'is_active', 'is_staff', 'date_joined', 'date_updated')
#     search_fields = ('first_name', 'last_name')
#     list_editable = ('is_active', 'is_staff', 'first_name', 'last_name')

#     list_filter = ('first_name', 'slug',)
#     empty_value_display = "undefined"


# class PatientAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'address', 'slug',)
#     list_display_links = ('user',)
#     list_editable = ('address',)

#     list_filter = ('user', 'address', 'slug',)


# class DoctorAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'spec', 'slug',)
#     list_display_links = ('user',)

#     list_filter = ('user', 'patients', 'slug',)


admin.site.register(CustomUser)
admin.site.register(PatientProfile)
admin.site.register(DoctorProfile)
admin.site.register(PatientCard)
