import os
import pickle
import numpy as np


def predict_anomaly(features: list):
    model_path = os.path.join(os.path.dirname(__file__), 'model', 'anomaly_prediction.pkl')
    with open(model_path, 'rb') as file:
        model = pickle.load(file)

    new_data = np.array(list(features)).reshape(1, -1)
    predicted_anomaly = model.predict(new_data)[0]
    return predicted_anomaly
