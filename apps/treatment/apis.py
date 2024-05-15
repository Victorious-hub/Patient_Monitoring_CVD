from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers

from apps.treatment.selectors import MedicationSelector, PrescriptionSelector
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
        prescription.create_prescription(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PrescriptionPatientListApi(views.APIView):
    class OutputSerializer(serializers.Serializer):
        medication = inline_serializer(fields={
            'name': serializers.CharField(),
            'dosage': serializers.CharField(),
            'description': serializers.CharField(),
            'created_at': serializers.DateTimeField(),
        })
        dosage = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

        class Meta:
            model = Prescription
            fields = ('medication', 'dosage', 'start_date', 'end_date', )

    def get(self, request, slug):
        prescriptions = PrescriptionSelector()
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
        print(request.data)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = TreatmentService(**serializer.validated_data)
        appointment.create_appointment(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        medications = MedicationSelector()
        data = self.OutputSerializer(medications.medication_list(), many=True).data
        return Response(data, status=status.HTTP_200_OK)
