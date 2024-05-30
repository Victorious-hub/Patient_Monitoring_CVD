from django.urls import path

from .apis import (
    AppointmentCreateApi,
    DoctorAppointmentListApi,
    MedicationListApi,
    PrescriptionCreateApi,
    MedicationCreateApi,
    PrescriptionPatientDeleteApi,
    PrescriptionPatientListApi,
    PatientAppointmentListApi,
)

urlpatterns = [
    path('v1/medications/create', MedicationCreateApi.as_view()),
    path('v1/prescriptions/<str:slug>/create', PrescriptionCreateApi.as_view()),
    path('v1/appointments/<str:slug>/create', AppointmentCreateApi.as_view()),
    path('v1/prescriptions/<str:slug>/get', PrescriptionPatientListApi.as_view()),
    path('v1/medications', MedicationListApi.as_view()),
    path('v1/appointments/<str:slug>', DoctorAppointmentListApi.as_view()),
    path('v1/prescriptions/decline/<str:slug>', PrescriptionPatientDeleteApi.as_view()),
    path('v1/appointments/patient/<str:slug>/get', PatientAppointmentListApi.as_view()),
]
