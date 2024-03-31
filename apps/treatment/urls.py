from django.urls import path

from .apis import (
    PrescriptionCreateApi,
    MedicationCreateApi,
)

urlpatterns = [
    path('v1/medications/create', MedicationCreateApi.as_view(), name='create_medication'),
    path('v1/prescriptions/<str:slug>/create', PrescriptionCreateApi.as_view(), name='create_prescription'),
]
