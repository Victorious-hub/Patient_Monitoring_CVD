from django.urls import path

from .apis import (
    CardCreateApi,
    CardDetailApi,
    CardListApi,
    DiseaseCreateApi,
    DiseaseDoctorDetailApi,
    PatientBloodCreateApi,
    PatientBloodDetailApi,
    PatientBloodListeApi,
    PatientCholesterolCreateApi,
    PatientCholesterolDetailApi,
)

urlpatterns = [
    path(
        'v1/patients/card/<str:slug>',
        CardCreateApi.as_view(),
        name='fill_patient_card'),
    path(
        'v1/patient/card',
        CardListApi.as_view(),
        name='patient_cards'),
    path(
        'v1/patient/card/<str:slug>',
        CardDetailApi.as_view(),
        name="patient_card"),
    path(
        'v1/patient/blood/analysis/<str:slug>',
        PatientBloodCreateApi.as_view(),
        name='patient_blood_analysis'),
    path(
        'v1/patient/blood/analysis',
        PatientBloodListeApi.as_view(),
        name='list_blood_analysis'),
    path(
        'v1/patient/cholesterol/analysis/<str:slug>',
        PatientCholesterolCreateApi.as_view(),
        name='create_cholesterol_analysis'),
    path(
        'v1/patient/blood/analysis/<str:slug>/get',
        PatientBloodDetailApi.as_view(),
        name='get_blood_analysis'),
    path(
        'v1/patient/disease/analysis/<str:slug>',
        DiseaseCreateApi.as_view(),
        name='disease_analysis'),
    path(
        'v1/patient/disease/analysis/<str:slug>/get',
        DiseaseDoctorDetailApi.as_view(),
        name='disease_analysis'),
    path(
        'v1/patient/cholesterol/analysis/<str:slug>/get',
        PatientCholesterolDetailApi.as_view(),
        name='cholesterol_list_analysis')]
