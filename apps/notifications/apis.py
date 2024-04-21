from rest_framework import views, serializers
from apps.notifications.models import Notification
from apps.notifications.selectors import NotificationSelector
from rest_framework import status
from rest_framework.response import Response


class NotificationListApi(views.APIView):
    class OutputSerializer(serializers.ModelSerializer):
        # patient = serializers.PrimaryKeyRelatedField(queryset=PatientProfile.objects.all())
        message = serializers.CharField()
        date_sent = serializers.DateField()
        is_read = serializers.BooleanField()

        class Meta:
            model = Notification
            fields = ('date_sent', 'message', 'is_read',)

    def get(self, request, slug):
        patient_notifications = NotificationSelector()
        data = self.OutputSerializer(patient_notifications.list(slug), many=True).data
        return Response(data, status=status.HTTP_200_OK)
