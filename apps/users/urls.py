from django.urls import path

from .apis import (
    DoctorCreateApi,
    DoctorDetailApi,
    DoctorListApi,
    DoctorPatientAddApi,
    DoctorPatientDeleteApi,
    DoctorPatientListApi,
    DoctorUpdateApi,
    HelloWorldView,
    PatientCreateApi,
    PatientDetailApi,
    PatientDoctorListApi,
    PatientListApi,
    PatientUpdateContactApi,
    ScheduleDetailApi,
    ScheduleListApi,
    ScheduleSignCreateApi,
)

urlpatterns = [

    path('about/', HelloWorldView.as_view()),


    path('v1/patients/registration', PatientCreateApi.as_view(), name='create_patient'),
    # path('v1/patients/update/<str:slug>/data', PatientUpdateDataApi.as_view(), name='data_update'),
    path('v1/patients/update/<str:slug>/contact', PatientUpdateContactApi.as_view(), name='contact_update'),
    # path('v1/patients/update/<str:slug>/password', PatientUpdatePasswordApi.as_view(), name='password_update'),
    path('v1/patients/', PatientListApi.as_view(), name='patients'),
    path('v1/patients/<str:slug>/get', PatientDetailApi.as_view(), name='get_patient'),
    # path('v1/patients/<str:slug>/update', PatientUpdatelApi.as_view(), name='update_patient'),

    path('v1/registration/doctor', DoctorCreateApi.as_view(), name='create_doctor'),
    path('v1/doctors', DoctorListApi.as_view(), name='list_doctor'),
    path('v1/doctors/<str:slug>/get', DoctorDetailApi.as_view(), name='get_doctor'),
    path('v1/doctors/<str:slug>/contact', DoctorUpdateApi.as_view(), name='contact_doctor_update'),
    path('v1/doctors/patient/<str:slug>/update', DoctorPatientAddApi.as_view(), name='add_doctor_patient_list'),
    path('v1/doctors/patient/<str:slug>/delete', DoctorPatientDeleteApi.as_view(), name='delete_patient'),
    path('v1/doctors/patient/<str:slug>/get', DoctorPatientListApi.as_view(), name='doctor_patients'),
    path('v1/patients/doctors/<str:slug>', PatientDoctorListApi.as_view(), name='patient_doctor_list'),
    path('v1/schedule', ScheduleListApi.as_view(), name='schedule'),
    path('v1/schedule/create/<str:slug>', ScheduleSignCreateApi.as_view()),
    path('v1/schedule/detail/<str:slug>', ScheduleDetailApi.as_view())
]
