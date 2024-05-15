from django.urls import path

from .apis import (
    AppointmentCreateApi,
    MedicationListApi,
    PrescriptionCreateApi,
    MedicationCreateApi,
    PrescriptionPatientListApi,
)

urlpatterns = [
    path('v1/medications/create', MedicationCreateApi.as_view(), name='create_medication'),
    path('v1/prescriptions/<str:slug>/create', PrescriptionCreateApi.as_view(), name='create_prescription'),
    path('v1/appointments/<str:slug>/create', AppointmentCreateApi.as_view(), name='create_appointment'),
    path('v1/prescriptions/<str:slug>/get', PrescriptionPatientListApi.as_view(), name='patient_prescriptions'),
    path('v1/medications', MedicationListApi.as_view(), name='medication_list')
]
