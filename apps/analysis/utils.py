import os
import pickle
import numpy as np

from apps.notifications.models import Notification
from apps.users.models import PatientProfile


def predict_anomaly(features: list):
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'anomaly_prediction.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    new_data = np.array(list(features)).reshape(1, -1)
    predicted_anomaly = model.predict(new_data)[0]
    return predicted_anomaly


def send_notification(notification_type: str, message: str, patient: PatientProfile):
    notification = Notification.objects.create(
        notification_type=notification_type,
        patient=patient,
        message=message,
        is_read=False,
    )

    notification.full_clean()
    notification.save()
