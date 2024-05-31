from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers

from apps.treatment.selectors import TreatmentSelector
from apps.users.apis import Base64ImageField
from apps.users.utils import inline_serializer
from apps.treatment.models import Appointment, Medication, Prescription
from apps.treatment.services import MedicationService, TreatmentService


class MedicationCreateApi(views.APIView):
    class InputSerializer(serializers.Serializer):
        name = serializers.CharField()
        dosage = serializers.CharField()
        description = serializers.CharField()
        created_at = serializers.DateField()

        class Meta:
            model = Medication
            fields = '__all__'

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        medication = MedicationService(**serializer.validated_data)
        medication.create_medication()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PrescriptionCreateApi(views.APIView):
    class InputSerializer(serializers.Serializer):
        patient_slug = serializers.CharField()
        medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all())
        dosage = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

        class Meta:
            model = Prescription
            fields = ('dosage', 'end_date', 'medication', 'patient_slug', 'start_date')

    def post(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prescription = TreatmentService(**serializer.validated_data)
        prescription.prescription_create(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PrescriptionPatientListApi(views.APIView):
    class OutputSerializer(serializers.Serializer):
        medication = inline_serializer(fields={
            'name': serializers.CharField(),
            'dosage': serializers.CharField(),
            'description': serializers.CharField(),
            'created_at': serializers.DateField(),
        })

        dosage = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()
        id = serializers.IntegerField()
        is_declined = serializers.BooleanField()

        class Meta:
            model = Prescription
            fields = ('is_declined', 'id', 'medication', 'dosage', 'start_date', 'end_date', )

    def get(self, request, slug):
        prescriptions = TreatmentSelector()
        data = self.OutputSerializer(prescriptions.patient_prescription_list(slug), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class AppointmentCreateApi(views.APIView):
    # permission_classes = (IsDoctor,)

    class InputSerializer(serializers.Serializer):
        patient_slug = serializers.CharField()
        appointment_date = serializers.DateField()
        appointment_time = serializers.TimeField()

        class Meta:
            model = Appointment
            fields = ('appointment_date', 'appointment_time', 'patient_slug',)

    def post(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = TreatmentService(**serializer.validated_data)
        appointment.appointment_create(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DoctorAppointmentListApi(views.APIView):
    # permission_classes = (IsDoctor,)

    class OutputSerializer(serializers.Serializer):
        appointment_date = serializers.DateField()
        appointment_time = serializers.TimeField()
        patient = inline_serializer(fields={
            'user': inline_serializer(fields={
                'first_name': serializers.CharField(),
                'last_name': serializers.CharField(),
                'email': serializers.CharField(),
            }),
        })

        class Meta:
            model = Appointment
            fields = ('appointment_date', 'appointment_time', 'patient',)

    def get(self, request, slug):
        appointment = TreatmentSelector()
        data = self.OutputSerializer(appointment.doctor_appointment_list(slug), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class MedicationListApi(views.APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        name = serializers.CharField()
        dosage = serializers.FloatField()
        description = serializers.CharField()
        created_at = serializers.DateField()

        class Meta:
            model = Medication
            fields = ('id', 'name', 'dosage', 'description', 'created_at', )

    def get(self, request):
        medications = TreatmentSelector()
        data = self.OutputSerializer(medications.medication_list(), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class PatientAppointmentListApi(views.APIView):
    # permission_classes = (IsDoctor,)

    class OutputSerializer(serializers.Serializer):
        doctor = inline_serializer(fields={
            'user': inline_serializer(fields={
                'first_name': serializers.CharField(),
                'last_name': serializers.CharField(),
                'email': serializers.CharField(),
            }),
            'profile_image': Base64ImageField(max_length=None, use_url=True)
        })
        appointment_date = serializers.DateField()
        appointment_time = serializers.TimeField()

        class Meta:
            model = Appointment
            fields = ('appointment_date', 'appointment_time', 'doctor',)

    def get(self, request, slug):
        appointments = TreatmentSelector()
        data = self.OutputSerializer(appointments.patient_appointment_list(slug), many=True).data
        return Response(data, status=status.HTTP_200_OK)


# class PrescriptionPatientDetailApi(views.APIView):
#     class Pagination(LimitOffsetPagination):
#         default_limit = 2

#     class OutputSerializer(serializers.Serializer):
#         medication = inline_serializer(fields={
#             'name': serializers.CharField(),
#             'dosage': serializers.CharField(),
#             'description': serializers.CharField(),
#             'created_at': serializers.DateField(),
#         })

#         dosage = serializers.CharField()
#         start_date = serializers.DateField()
#         end_date = serializers.DateField()

#         class Meta:
#             model = Prescription
#             fields = ('medication', 'dosage', 'start_date', 'end_date', )

#     def get(self, request, slug):
#         prescriptions = TreatmentSelector()
#         data = self.OutputSerializer(prescriptions.doctor_prescription_list(slug), many=True).data

#         return get_paginated_response(
#             pagination_class=self.Pagination,
#             serializer_class=self.OutputSerializer,
#             queryset=data,
#             request=request,
#             view=self
#         )


class PrescriptionPatientDeleteApi(views.APIView):
    class InputSerializer(serializers.Serializer):
        patient_slug = serializers.CharField()
        id = serializers.IntegerField()

        class Meta:
            model = Prescription
            fields = ('patient_slug', 'id',)

    def put(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = TreatmentService(**serializer.validated_data)
        appointment.prescription_decline(slug)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
