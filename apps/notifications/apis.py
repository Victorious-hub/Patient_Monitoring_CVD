from rest_framework import views, serializers
from apps.notifications.models import Notification
from apps.notifications.selectors import NotificationSelector
from apps.notifications.services import NotificationService
from apps.users.models import PatientProfile
from rest_framework import status
from rest_framework.response import Response


class NotificationCreateApi(views.APIView):
    class InputSerializer(serializers.ModelSerializer):
        patient = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all(), many=False)
        message = serializers.CharField()
        is_read = serializers.BooleanField()

        class Meta:
            model = Notification
            fields = ('patient', 'message', 'is_read',)

    def post(self, request, slug):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        notification = NotificationService(**serializer.validated_data)
        notification.send_notification(slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotificationListApi(views.APIView):
    class OutputSerializer(serializers.ModelSerializer):
        patient = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all(), many=False)
        message = serializers.CharField()
        is_read = serializers.BooleanField()

        class Meta:
            model = Notification
            fields = ('patient', 'message', 'is_read',)

    def get(self, request, slug):
        patient_notifications = NotificationSelector()
        data = self.OutputSerializer(patient_notifications.list(slug), many=True).data
        return Response(data, status=status.HTTP_200_OK)
