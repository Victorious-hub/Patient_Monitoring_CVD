from celery import shared_task
import pickle
import os
import numpy as np

from apps.notifications.models import Notification


@shared_task()
def predict_anomaly(features: list):
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'anomaly_prediction.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)
    print(features)
    new_data = np.array(list(features)).reshape(1, -1)
    predicted_anomaly = model.predict(new_data)[0]
    return predicted_anomaly


@shared_task()
def send_analysis_result(slug: str) -> Notification:
    pass
