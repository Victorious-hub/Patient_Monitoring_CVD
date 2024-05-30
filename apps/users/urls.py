from django.urls import path

from .apis import (
    DoctorCreateApi,
    DoctorDetailApi,
    DoctorListApi,
    DoctorPatientDeleteApi,
    DoctorPatientListApi,
    DoctorUpdateApi,
    HelloWorldView,
    PatientCreateApi,
    PatientDetailApi,
    PatientDoctorListApi,
    PatientListApi,
    PatientUpdateContactApi,
    ScheduleListApi,
    ScheduleSignCreateApi,
)

urlpatterns = [

    path('about/', HelloWorldView.as_view()),


    path('v1/patients/registration', PatientCreateApi.as_view()),
    path('v1/patients/update/<str:slug>/contact', PatientUpdateContactApi.as_view()),
    path('v1/patients/', PatientListApi.as_view()),
    path('v1/patients/<str:slug>/get', PatientDetailApi.as_view()),

    path('v1/registration/doctor', DoctorCreateApi.as_view()),
    path('v1/doctors', DoctorListApi.as_view()),
    path('v1/doctors/<str:slug>/get', DoctorDetailApi.as_view()),
    path('v1/doctors/<str:slug>/contact', DoctorUpdateApi.as_view()),
    path('v1/doctors/patient/<str:slug>/delete', DoctorPatientDeleteApi.as_view()),
    path('v1/doctors/patient/<str:slug>/get', DoctorPatientListApi.as_view()),
    path('v1/patients/doctors/<str:slug>', PatientDoctorListApi.as_view()),
    path('v1/schedule', ScheduleListApi.as_view()),
    path('v1/schedule/create/<str:slug>', ScheduleSignCreateApi.as_view()),
]
