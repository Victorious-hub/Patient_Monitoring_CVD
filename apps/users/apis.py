import logging
from django.views.generic import TemplateView
from rest_framework import views
from rest_framework import status

from rest_framework.response import Response
from rest_framework import serializers
from apps.users.constansts import GENDER
from apps.users.services import (
    # DoctorService,
    DoctorService,
    PatientService,
    RegistrationService,
)

from apps.users.selectors import (
    DoctorSelector,
    PatientSelector
)
from apps.users.utils import inline_serializer

from .models import (
    PatientProfile,
    DoctorProfile
)

logger = logging.getLogger(__name__)


class HelloWorldView(TemplateView):
    template_name = 'test.html'


class PatientCreateApi(views.APIView):
    class InputSerializer(serializers.ModelSerializer):
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
            'password': serializers.CharField(),
        })

        class Meta:
            model = PatientProfile
            fields = ('user',)

    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        patient = RegistrationService(**serializer.validated_data)
        patient.patient_create()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientUpdateDataApi(views.APIView):
    # permission_classes = (IsPatient,)

    class InputSerializer(serializers.ModelSerializer):
        weight = serializers.FloatField(),
        height = serializers.IntegerField(),
        age = serializers.IntegerField(),
        gender = serializers.ChoiceField(choices=GENDER)
        birthday = serializers.DateField(),

        class Meta:
            model = PatientProfile
            fields = ('weight', 'height', 'gender', 'age', 'birthday')

    def put(self, request, slug):
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        patient_service = PatientService(**serializer.validated_data)
        patient_service.patient_update_data(slug)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientUpdateContactApi(views.APIView):
    # permission_classes = (IsPatient,)

    class InputSerializer(serializers.ModelSerializer):
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        })
        mobile = serializers.CharField()

        class Meta:
            model = PatientProfile
            fields = ('user', 'mobile',)

    def put(self, request, slug):
        print(request.data)
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        patient = PatientService(**serializer.validated_data)
        patient.patient_update_contact(slug)
        return Response(serializer.data, status=status.HTTP_200_OK)


# class PatientUpdatePasswordApi(views.APIView):
#     #permission_classes = (IsPatient,)

#     class InputSerializer(serializers.Serializer):
#         password_confirm = serializers.CharField(),
#         new_password = serializers.CharField(),
#         user = inline_serializer(fields={
#             'password': serializers.CharField(),
#         })

#         class Meta:
#             model = PatientProfile
#             fields = ('user', 'new_password', 'password_confirm',)

#     def put(self, request, slug):
#         serializer = self.InputSerializer(data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         patient = PatientService(**serializer.validated_data)
#         patient.password_update(slug)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class PatientListApi(views.APIView):
    # permission_classes = (IsPatient,)

    class OutputSerializer(serializers.ModelSerializer):
        weight = serializers.FloatField(),
        height = serializers.IntegerField(),
        age = serializers.IntegerField(),
        gender = serializers.ChoiceField(choices=GENDER)
        birthday = serializers.DateField(),
        slug = serializers.CharField(),
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
            'role': serializers.CharField(),
        })

        class Meta:
            model = PatientProfile
            fields = ('user', 'weight', 'height', 'gender', 'age', 'birthday', 'slug',)

    def get(self, request):
        patients = PatientSelector()
        data = self.OutputSerializer(patients.patient_list(), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class PatientDetailApi(views.APIView):
    # permission_classes = (IsPatient,)

    class OutputSerializer(serializers.ModelSerializer):
        weight = serializers.FloatField(),
        height = serializers.IntegerField(),
        age = serializers.IntegerField(),
        gender = serializers.ChoiceField(choices=GENDER)
        birthday = serializers.DateField(),
        slug = serializers.CharField(),
        mobile = serializers.CharField(),
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        })

        class Meta:
            model = PatientProfile
            fields = ('user', 'weight', 'height', 'gender', 'age', 'birthday', 'slug', 'mobile',)

    def get(self, request, slug):
        patients = PatientSelector()
        data = self.OutputSerializer(patients.patient_get(slug=slug)).data
        return Response(data, status=status.HTTP_200_OK)


class DoctorCreateApi(views.APIView):
    class InputSerializer(serializers.ModelSerializer):
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
            'password': serializers.CharField(),
        })

        class Meta:
            model = DoctorProfile
            fields = ('user',)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = RegistrationService(**serializer.validated_data)
        doctor.doctor_create()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DoctorListApi(views.APIView):
    # permission_classes = (IsDoctor,)

    class OutputSerializer(serializers.ModelSerializer):
        patients = inline_serializer(fields={
            'user.first_name': serializers.CharField(),
            'user.last_name': serializers.CharField(),
            'user.email': serializers.EmailField(),
            'height': serializers.IntegerField(),
            'weight': serializers.FloatField(),
            'gender': serializers.ChoiceField(choices=GENDER),
            'age': serializers.IntegerField(),
            'birthday': serializers.DateField(),
        }, many=True)
        patient_cards = inline_serializer(fields={
            'blood_type': serializers.BooleanField(),
            'allergies': serializers.JSONField(),
            'abnormal_conditions': serializers.CharField(),
            'smoke': serializers.BooleanField(),
            'alcohol': serializers.BooleanField(),
        }, many=True)
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        })

        class Meta:
            model = DoctorProfile
            fields = ('user', 'patients', 'patient_cards',)

    def get(self, request):
        doctors = DoctorSelector()
        data = self.OutputSerializer(doctors.doctor_list(), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class DoctorDetailApi(views.APIView):
    # permission_classes = (IsDoctor,)

    class OutputSerializer(serializers.ModelSerializer):
        patients = inline_serializer(fields={
            'user.first_name': serializers.CharField(),
            'user.last_name': serializers.CharField(),
            'user.email': serializers.EmailField(),
            'height': serializers.IntegerField(),
            'weight': serializers.FloatField(),
            'gender': serializers.ChoiceField(choices=GENDER),
            'age': serializers.IntegerField(),
            'birthday': serializers.DateField(),
        }, many=True)
        patient_cards = inline_serializer(fields={
            'blood_type': serializers.BooleanField(),
            'allergies': serializers.JSONField(),
            'abnormal_conditions': serializers.CharField(),
            'smoke': serializers.BooleanField(),
            'alcohol': serializers.BooleanField(),
        }, many=True)
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        })

        class Meta:
            model = DoctorProfile
            fields = ('user', 'patients', 'patient_cards',)

    def get(self, request, slug):
        doctors = DoctorSelector()
        data = self.OutputSerializer(doctors.doctor_get(slug=slug)).data
        return Response(data, status=status.HTTP_200_OK)


class DoctorUpdateApi(views.APIView):
    # permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        })

        class Meta:
            model = DoctorProfile
            fields = ('user',)

    def put(self, request, slug):
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        doctor = DoctorService(**serializer.validated_data)
        doctor.doctor_contact_update(slug)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorPatientAddApi(views.APIView):
    # permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        patients = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all(), many=True)

        class Meta:
            model = DoctorProfile
            fields = ('patients',)

    def put(self, request, slug):
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        doctor = DoctorService(**serializer.validated_data)
        doctor.patient_list_update(slug=slug)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DoctorPatientDeleteApi(views.APIView):
    # permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        patients = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all())

        class Meta:
            model = DoctorProfile
            fields = ('patients',)

    def delete(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = DoctorService(**serializer.validated_data)
        doctor.patient_remove(slug=slug)
        return Response(status=status.HTTP_204_NO_CONTENT)


class DoctorPatientListApi(views.APIView):
    class OutputSerializer(serializers.Serializer):
        patients = inline_serializer(fields={
            'user.first_name': serializers.CharField(),
            'user.last_name': serializers.CharField(),
            'user.email': serializers.EmailField(),
            'height': serializers.IntegerField(),
            'weight': serializers.FloatField(),
            'gender': serializers.ChoiceField(choices=GENDER),
            'age': serializers.IntegerField(),
            'birthday': serializers.DateField(),
        }, many=True)

    class Meta:
        model = DoctorProfile
        fields = ('patients',)

    def get(self, request, slug):
        doctors = DoctorSelector()
        data = self.OutputSerializer(doctors.doctor_get_patients(slug)).data
        return Response(data, status=status.HTTP_200_OK)
