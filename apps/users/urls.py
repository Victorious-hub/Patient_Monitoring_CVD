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

    path('about/', HelloWorldView.as_view(), name='about'),
    path('v1/patients/registration', PatientCreateApi.as_view(), name='registration'),
    path('v1/patients/update/<str:slug>/contact', PatientUpdateContactApi.as_view()),
    path('v1/patients/', PatientListApi.as_view(), name='patients'),
    path('v1/patients/<str:slug>/get', PatientDetailApi.as_view(), name='patient_detail'),

    path('v1/registration/doctor', DoctorCreateApi.as_view()),
    path('v1/doctors', DoctorListApi.as_view(), name='doctors'),
    path('v1/doctors/<str:slug>/get', DoctorDetailApi.as_view(), name='doctor_detail'),
    path('v1/doctors/<str:slug>/contact', DoctorUpdateApi.as_view()),
    path('v1/doctors/patient/<str:slug>/delete', DoctorPatientDeleteApi.as_view()),
    path('v1/doctors/patient/<str:slug>/get', DoctorPatientListApi.as_view(), name='doctor_patients'),
    path('v1/patients/doctors/<str:slug>', PatientDoctorListApi.as_view(), name='patient_doctors'),
    path('v1/schedule', ScheduleListApi.as_view(), name='schedule'),
    path('v1/schedule/create/<str:slug>', ScheduleSignCreateApi.as_view()),
]
