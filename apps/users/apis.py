import logging
import base64
import six
import uuid
import imghdr
from django.views.generic import TemplateView
from rest_framework import views
from rest_framework import status
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework import serializers
from .permissions import IsPatient, IsDoctor
from .selectors import DoctorSelector, PatientSelector
from .utils import inline_serializer
from .models import PatientProfile, DoctorProfile
from .services import (
    DoctorService,
    PatientService,
    RegistrationService,
)
from apps.treatment.models import Appointment

logger = logging.getLogger(__name__)


class HelloWorldView(TemplateView):
    template_name = 'test.html'


class Base64ImageField(serializers.ImageField):

    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            if 'data:' in data and ';base64,' in data:
                header, data = data.split(';base64,')
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension, )
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension


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


class PatientUpdateContactApi(views.APIView):
    # permission_classes = (IsPatient,)

    class InputSerializer(serializers.ModelSerializer):
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
        })
        mobile = serializers.CharField()
        address = serializers.CharField()

        class Meta:
            model = PatientProfile
            fields = ('user', 'mobile', 'address', )

    def put(self, request, slug):
        print(request.data)
        serializer = self.InputSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        patient = PatientService(**serializer.validated_data)
        patient.patient_update_contact(slug)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientListApi(views.APIView):
    permission_classes = (IsPatient | IsDoctor,)

    class OutputSerializer(serializers.ModelSerializer):
        mobile = serializers.CharField(),
        address = serializers.CharField(),
        slug = serializers.CharField(),
        has_card = serializers.BooleanField(),
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
            'role': serializers.CharField(),
        })

        class Meta:
            model = PatientProfile
            fields = ('user', 'mobile', 'address', 'slug', 'has_card',)

    def get(self, request):
        patients = PatientSelector()
        data = self.OutputSerializer(patients.patient_list(), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class PatientDetailApi(views.APIView):
    permission_classes = (IsPatient | IsDoctor,)

    class OutputSerializer(serializers.ModelSerializer):
        mobile = serializers.CharField(),
        address = serializers.CharField(),
        slug = serializers.CharField(),
        has_card = serializers.BooleanField()
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
            'role': serializers.CharField(),
        })

        class Meta:
            model = PatientProfile
            fields = ('user', 'mobile', 'address', 'slug', 'has_card',)

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
        experience = serializers.IntegerField()
        description = serializers.CharField()

        class Meta:
            model = DoctorProfile
            fields = ('user', 'experience', 'description',)

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = RegistrationService(**serializer.validated_data)
        doctor.doctor_create()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DoctorListApi(views.APIView):
    class OutputSerializer(serializers.ModelSerializer):
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        })
        profile_image = Base64ImageField(max_length=None, use_url=True)

        class Meta:
            model = DoctorProfile
            fields = ('user', 'profile_image',)

    def get(self, request):
        doctors = DoctorSelector()
        data = self.OutputSerializer(doctors.doctor_list(), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class PatientDoctorListApi(views.APIView):
    permission_classes = (IsDoctor | IsPatient,)

    class OutputSerializer(serializers.ModelSerializer):
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        })
        profile_image = Base64ImageField(max_length=None, use_url=True)
        description = serializers.CharField()

        class Meta:
            model = DoctorProfile
            fields = ('user', 'profile_image', 'description',)

    def get(self, request, slug):
        patients = PatientSelector()
        data = self.OutputSerializer(patients.patient_doctor_list(slug), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class DoctorDetailApi(views.APIView):
    permission_classes = (IsDoctor,)

    class OutputSerializer(serializers.ModelSerializer):
        profile_image = Base64ImageField(max_length=None, use_url=True)
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
            'email': serializers.EmailField(),
        })
        experience = serializers.IntegerField()
        description = serializers.CharField()

        class Meta:
            model = DoctorProfile
            fields = ('user', 'profile_image', 'experience', 'description',)

    def get(self, request, slug):
        doctors = DoctorSelector()
        data = self.OutputSerializer(doctors.doctor_get(slug=slug)).data
        return Response(data, status=status.HTTP_200_OK)


class DoctorUpdateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        user = inline_serializer(fields={
            'first_name': serializers.CharField(),
            'last_name': serializers.CharField(),
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


class DoctorPatientDeleteApi(views.APIView):
    permission_classes = (IsDoctor,)

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
    permission_classes = (IsDoctor | IsPatient,)

    class OutputSerializer(serializers.Serializer):
        patients = inline_serializer(fields={
            'user': inline_serializer(fields={
                'first_name': serializers.CharField(),
                'last_name': serializers.CharField(),
                'email': serializers.CharField(),
            }),
        }, many=True)

        class Meta:
            model = DoctorProfile
            fields = ('patients',)

    def get(self, request, slug):
        doctors = DoctorSelector()
        data = self.OutputSerializer(doctors.doctor_get_patients(slug)).data
        return Response(data, status=status.HTTP_200_OK)


class DoctorPatientDetailApi(views.APIView):
    permission_classes = (IsDoctor | IsPatient,)

    class OutputSerializer(serializers.Serializer):
        patients = inline_serializer(fields={
            'user': inline_serializer(fields={
                'first_name': serializers.CharField(),
                'last_name': serializers.CharField(),
                'email': serializers.CharField(),
            }),
        },)

        class Meta:
            model = DoctorProfile
            fields = ('patients',)

    def get(self, request, slug):
        doctors = DoctorSelector()
        data = self.OutputSerializer(doctors.doctor_get_patients(slug)).data
        return Response(data, status=status.HTTP_200_OK)


class ScheduleListApi(views.APIView):
    permission_classes = (IsDoctor | IsPatient,)

    class OutputSerializer(serializers.ModelSerializer):
        doctor = inline_serializer(fields={
            'profile_image': Base64ImageField(max_length=None, use_url=True),
            'description': serializers.CharField(),
            'experience': serializers.IntegerField(),
            'user': inline_serializer(fields={
                'first_name': serializers.CharField(),
                'last_name': serializers.CharField(),
                'email': serializers.CharField(),
            }),
        })
        available_time = serializers.JSONField()

        class Meta:
            model = DoctorProfile
            fields = ('doctor', 'available_time',)

    def get(self, request):
        doctors = DoctorSelector()
        data = self.OutputSerializer(doctors.schedule_list(), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class ScheduleSignCreateApi(views.APIView):
    permission_classes = (IsDoctor | IsPatient,)

    class InputSerializer(serializers.Serializer):
        doctor_slug = serializers.CharField()
        appointment_date = serializers.CharField()
        appointment_time = serializers.CharField()

        class Meta:
            model = Appointment
            fields = ('doctor_slug', 'appointment_date', 'appointment_time',)

    def post(self, request, slug):
        print(request.data)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = DoctorService(**serializer.validated_data)
        appointment.appointment_create(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
