from django.urls import path

from .apis import (
    CardCreateApi,
    CardDetailApi,
    CardListApi,
    CardUpdateApi,
    ConclusionCreateApi,
    DiagnosisCreateApi,
    DoctorPatientBloodDetailApi,
    DoctorPatientCholesterolDetailApi,
    PatientBloodCreateApi,
    PatientBloodDetailApi,
    PatientBloodUpdateApi,
    PatientCholesterolCreateApi,
    PatientCholesterolDetailApi,
    PatientCholesterolUpdateApi,
    PatientConclusionDetailApi,
    PatientDiagnosisDetailApi,
)

urlpatterns = [
    path('v1/patients/card/<str:slug>', CardCreateApi.as_view()),
    path('v1/patient/card', CardListApi.as_view()),
    path('v1/patient/card/<str:slug>', CardDetailApi.as_view()),
    path('v1/patient/card/<str:slug>/update', CardUpdateApi.as_view()),
    path('v1/patient/blood/analysis/<str:slug>', PatientBloodCreateApi.as_view()),
    path('v1/patient/cholesterol/analysis/<str:slug>', PatientCholesterolCreateApi.as_view(),
         name='create_cholesterol_analysis'),
    path('v1/patient/blood/<str:slug>/get', PatientBloodDetailApi.as_view()),
    path('v1/patient/conclusion/<str:slug>/create', ConclusionCreateApi.as_view()),
    path('v1/patient/cholesterol/<str:slug>/get', PatientCholesterolDetailApi.as_view()),
    path('v1/patient/diagnosis/<str:slug>', PatientDiagnosisDetailApi.as_view()),
    path('v1/patient/conclusion/<str:slug>/get', PatientConclusionDetailApi.as_view()),
    path('v1/cholesterol/<str:slug>/update', PatientCholesterolUpdateApi.as_view()),
    path('v1/blood/<str:slug>/update', PatientBloodUpdateApi.as_view()),
    path('v1/blood/<str:slug>/get/last', DoctorPatientBloodDetailApi.as_view()),
    path('v1/cholesterol/<str:slug>/get/last', DoctorPatientCholesterolDetailApi.as_view()),
    path('v1/diagnosis/<str:slug>/create', DiagnosisCreateApi.as_view())
]
