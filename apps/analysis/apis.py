from rest_framework import views
from rest_framework import serializers

from .permissions import IsDoctor, IsPatient
from .selectors import AnalysisSelector
from .services import AnalysisService
from rest_framework.response import Response
from rest_framework import status

from apps.users.apis import Base64ImageField
from apps.users.utils import inline_serializer

from .models import (
    BloodAnalysis,
    CholesterolAnalysis,
    Conclusion,
    Diagnosis,
    PatientCard
)


class PatientBloodCreateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        ap_hi = serializers.IntegerField()
        ap_lo = serializers.IntegerField()
        glucose = serializers.FloatField()
        patient_slug = serializers.CharField()

        class Meta:
            model = BloodAnalysis
            fields = ('ap_hi', 'ap_lo', 'glucose', 'patient_slug',)

    def post(self, request, slug):
        print(request.data)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = AnalysisService(**serializer.validated_data)
        patient.blood_analysis_create(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientBloodDetailApi(views.APIView):
    permission_classes = (IsDoctor | IsPatient,)

    class OutputSerializer(serializers.ModelSerializer):
        glucose = serializers.FloatField()
        ap_hi = serializers.IntegerField()
        ap_lo = serializers.IntegerField()
        created_at = serializers.DateField()

        class Meta:
            model = BloodAnalysis
            fields = ('created_at', 'glucose', 'ap_hi', 'ap_lo',)

    def get(self, request, slug):
        patient_blood = AnalysisSelector()
        data = self.OutputSerializer(patient_blood.blood_analysis_get(slug), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class PatientCholesterolCreateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        patient_slug = serializers.CharField()
        cholesterol = serializers.FloatField()
        hdl_cholesterol = serializers.FloatField()
        ldl_cholesterol = serializers.FloatField()
        triglycerides = serializers.FloatField()

        class Meta:
            model = CholesterolAnalysis
            fields = ('cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'patient_slug', 'triglycerides',)

    def post(self, request, slug):
        print(request.data)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = AnalysisService(**serializer.validated_data)
        patient.chol_analysis_create(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientCholesterolUpdateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        cholesterol = serializers.FloatField()
        hdl_cholesterol = serializers.FloatField()
        ldl_cholesterol = serializers.FloatField()
        triglycerides = serializers.FloatField()

        class Meta:
            model = CholesterolAnalysis
            fields = ('cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',)

    def put(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = AnalysisService(**serializer.validated_data)
        patient.chol_analysis_update(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientBloodUpdateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        glucose = serializers.FloatField()
        ap_hi = serializers.IntegerField()
        ap_lo = serializers.IntegerField()

        class Meta:
            model = BloodAnalysis
            fields = ('glucose', 'ap_hi', 'ap_lo',)

    def put(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = AnalysisService(**serializer.validated_data)
        patient.blood_analysis_update(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientCholesterolDetailApi(views.APIView):
    permission_classes = (IsPatient | IsDoctor,)

    class OutputSerializer(serializers.ModelSerializer):
        cholesterol = serializers.FloatField()
        hdl_cholesterol = serializers.FloatField()
        ldl_cholesterol = serializers.FloatField()
        triglycerides = serializers.FloatField()
        created_at = serializers.DateField()

        class Meta:
            model = BloodAnalysis
            fields = ('created_at', 'cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',)

    def get(self, request, slug):
        patient_blood = AnalysisSelector()
        data = self.OutputSerializer(patient_blood.cholesterol_analysis_get(slug), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class CardCreateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        patient_slug = serializers.CharField()
        smoke = serializers.BooleanField()
        alcohol = serializers.BooleanField()
        blood_type = serializers.ChoiceField(choices=PatientCard.BloodType.choices)
        abnormal_conditions = serializers.CharField()
        active = serializers.BooleanField()
        height = serializers.IntegerField()
        weight = serializers.FloatField()
        gender = serializers.ChoiceField(choices=PatientCard.GenderType.choices)
        birthday = serializers.DateField()

        class Meta:
            model = PatientCard
            fields = (
                'patient_slug',
                'smoke',
                'alcohol',
                'blood_type',
                'abnormal_conditions',
                'active',
                'weight',
                'height',
                'gender',
                'birthday',
            )

    def post(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        doctor = AnalysisService(**validated_data)
        doctor.card_create(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CardUpdateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.ModelSerializer):
        patient_slug = serializers.CharField()
        smoke = serializers.BooleanField()
        alcohol = serializers.BooleanField()
        blood_type = serializers.ChoiceField(choices=PatientCard.BloodType.choices)
        abnormal_conditions = serializers.CharField()
        active = serializers.BooleanField()
        height = serializers.IntegerField()
        weight = serializers.FloatField()
        gender = serializers.ChoiceField(choices=PatientCard.GenderType.choices)
        birthday = serializers.DateField()

        class Meta:
            model = PatientCard
            fields = '__all__'

    def put(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        doctor = AnalysisService(**validated_data)
        doctor.card_update(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CardListApi(views.APIView):
    permission_classes = (IsDoctor | IsPatient,)

    class OutputSerializer(serializers.ModelSerializer):
        patient = inline_serializer(fields={
            'user': inline_serializer(fields={
                'first_name': serializers.CharField(),
                'last_name': serializers.CharField(),
                'email': serializers.CharField(),
            }),
        })
        smoke = serializers.FloatField()
        active = serializers.FloatField()
        alcohol = serializers.FloatField()
        blood_type = serializers.ChoiceField(choices=PatientCard.BloodType.choices)
        abnormal_conditions = serializers.CharField()
        age = serializers.IntegerField()
        height = serializers.IntegerField()
        weight = serializers.IntegerField()
        birthday = serializers.DateField()
        gender = serializers.ChoiceField(choices=PatientCard.GenderType.choices)
        is_cholesterol_analysis = serializers.BooleanField()
        is_blood_analysis = serializers.BooleanField()
        is_confirmed = serializers.BooleanField()

        class Meta:
            model = PatientCard
            fields = '__all__'

    def get(self, request):
        patients = AnalysisSelector()
        data = self.OutputSerializer(patients.card_list(), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class CardDetailApi(views.APIView):
    permission_classes = (IsPatient | IsDoctor,)

    class OutputSerializer(serializers.Serializer):
        patient = inline_serializer(fields={
            'user': inline_serializer(fields={
                'first_name': serializers.CharField(),
                'last_name': serializers.CharField(),
                'email': serializers.CharField(),
            }),
        })
        smoke = serializers.FloatField()
        active = serializers.FloatField()
        alcohol = serializers.FloatField()
        blood_type = serializers.ChoiceField(choices=PatientCard.BloodType.choices)
        abnormal_conditions = serializers.CharField()
        age = serializers.IntegerField()
        height = serializers.IntegerField()
        weight = serializers.IntegerField()
        birthday = serializers.DateField()
        gender = serializers.ChoiceField(choices=PatientCard.GenderType.choices)
        is_cholesterol_analysis = serializers.BooleanField()
        is_blood_analysis = serializers.BooleanField()
        is_confirmed = serializers.BooleanField()

        class Meta:
            model = PatientCard
            fields = (
                '__all__'
            )

    def get(self, request, slug):
        patients = AnalysisSelector()
        data = self.OutputSerializer(patients.patient_get_card(slug=slug)).data
        return Response(data, status=status.HTTP_200_OK)


class ConclusionCreateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.Serializer):
        patient_slug = serializers.CharField()
        description = serializers.CharField()
        recommendations = serializers.CharField()

        class Meta:
            model = Conclusion
            fields = ('patient_slug', 'description', 'recommendations',)

    def post(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prescription = AnalysisService(**serializer.validated_data)
        prescription.conclusion_create(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ConfirmAnalysisCreateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.Serializer):
        patient_slug = serializers.CharField()
        description = serializers.CharField()
        recommendations = serializers.CharField()

        class Meta:
            model = Conclusion
            fields = ('patient_slug', 'description', 'recommendations',)

    def post(self, request, slug):
        print(request.data)
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prescription = AnalysisService(**serializer.validated_data)
        prescription.conclusion_create(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientDiagnosisDetailApi(views.APIView):
    permission_classes = (IsDoctor | IsPatient,)

    class OutputSerializer(serializers.ModelSerializer):
        blood_analysis = inline_serializer(fields={
            'glucose': serializers.FloatField(),
            'ap_hi': serializers.IntegerField(),
            'ap_lo': serializers.IntegerField(),
        })
        cholesterol_analysis = inline_serializer(fields={
            'cholesterol': serializers.FloatField(),
            'hdl_cholesterol': serializers.FloatField(),
            'ldl_cholesterol': serializers.FloatField(),
            'triglycerides': serializers.FloatField(),
        })
        anomaly = serializers.BooleanField()

        class Meta:
            model = Diagnosis
            fields = ('anomaly', 'blood_analysis', 'cholesterol_analysis',)

    def get(self, request, slug):
        patients = AnalysisSelector()
        data = self.OutputSerializer(patients.patient_diagnosis_get(slug)).data
        return Response(data, status=status.HTTP_200_OK)


class PatientConclusionDetailApi(views.APIView):
    permission_classes = (IsDoctor | IsPatient,)

    class OutputSerializer(serializers.ModelSerializer):
        doctor = inline_serializer(fields={
            'user': inline_serializer(fields={
                'first_name': serializers.CharField(),
                'last_name': serializers.CharField(),
                'email': serializers.CharField(),
            }),
            'profile_image': Base64ImageField(max_length=None, use_url=True)
        },)
        analysis_result = inline_serializer(fields={
            'blood_analysis': inline_serializer(fields={
                'glucose': serializers.FloatField(),
                'ap_hi': serializers.IntegerField(),
                'ap_lo': serializers.IntegerField(),
                'created_at': serializers.DateField()
            }),
            'cholesterol_analysis': inline_serializer(fields={
                'cholesterol': serializers.FloatField(),
                'hdl_cholesterol': serializers.FloatField(),
                'ldl_cholesterol': serializers.FloatField(),
                'triglycerides': serializers.FloatField(),
                'created_at': serializers.DateField()
            }),
            'anomaly': serializers.BooleanField()
        },)
        description = serializers.CharField()
        recommendations = serializers.CharField()
        created_at = serializers.DateField()

        class Meta:
            model = Conclusion
            fields = '__all__'

    def get(self, request, slug):
        patients = AnalysisSelector()
        data = self.OutputSerializer(patients.patient_conclusions_get(slug), many=True).data
        return Response(data, status=status.HTTP_200_OK)


class DoctorPatientBloodDetailApi(views.APIView):
    permission_classes = (IsDoctor,)

    class OutputSerializer(serializers.ModelSerializer):
        glucose = serializers.FloatField()
        ap_hi = serializers.IntegerField()
        ap_lo = serializers.IntegerField()
        created_at = serializers.DateField()

        class Meta:
            model = BloodAnalysis
            fields = ('created_at', 'glucose', 'ap_hi', 'ap_lo',)

    def get(self, request, slug):
        patient_blood = AnalysisSelector()
        data = self.OutputSerializer(patient_blood.doctor_patient_blood_get(slug)).data
        return Response(data, status=status.HTTP_200_OK)


class DoctorPatientCholesterolDetailApi(views.APIView):
    permission_classes = (IsDoctor,)

    class OutputSerializer(serializers.ModelSerializer):
        cholesterol = serializers.FloatField()
        hdl_cholesterol = serializers.FloatField()
        ldl_cholesterol = serializers.FloatField()
        triglycerides = serializers.FloatField()

        class Meta:
            model = BloodAnalysis
            fields = ('cholesterol', 'hdl_cholesterol', 'ldl_cholesterol', 'triglycerides',)

    def get(self, request, slug):
        patient_cholesterol = AnalysisSelector()
        data = self.OutputSerializer(patient_cholesterol.doctor_patient_cholesterol_get(slug)).data
        return Response(data, status=status.HTTP_200_OK)


class DiagnosisCreateApi(views.APIView):
    permission_classes = (IsDoctor,)

    class InputSerializer(serializers.Serializer):
        patient_slug = serializers.CharField()

        class Meta:
            model = Diagnosis
            fields = ('patient_slug',)

    def post(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = AnalysisService(**serializer.validated_data)
        appointment.disease_create(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
