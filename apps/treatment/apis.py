from rest_framework import views
from rest_framework import status
from rest_framework.response import Response
from rest_framework import serializers

from apps.treatment.selectors import PrescriptionSelector
from apps.users.utils import inline_serializer
from permissions.doctor_permission import IsDoctor
from apps.treatment.models import Appointment, Medication, Prescription
from apps.treatment.services import MedicationService, TreatmentService
from apps.users.models import PatientCard


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
        patient_card = serializers.PrimaryKeyRelatedField(queryset=PatientCard.objects.all())
        medication = serializers.PrimaryKeyRelatedField(queryset=Medication.objects.all())
        dosage = serializers.CharField()
        start_date = serializers.DateField()
        end_date = serializers.DateField()

        class Meta:
            model = Prescription
            fields = '__all__'

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
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.Serializer):
        patient_card = serializers.PrimaryKeyRelatedField(queryset=PatientCard.objects.all())
        appointment_date = serializers.DateField()
        appointment_time = serializers.TimeField()

        class Meta:
            model = Appointment
            fields = '__all__'

    def post(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = TreatmentService(**serializer.validated_data)
        appointment.create_appointment(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
