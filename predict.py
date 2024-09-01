import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import MeanSquaredError
import joblib


model = None
scaler = None
fish_species = ['Atlantic Mackerel', 'Bigeye Tuna', 'Longfin Mako Shark', 'Orange Roughy', 'Pacific Mackerel',
                'Prionace glauca', 'Scalloped Hammerhead', 'Southern Bluefin Tuna', 'Swordfish', 'Yellowfin Tuna']
SQUARE_MILES = 5


def load_prediction_model():
    global model, scaler
    print("Loading Model...")
    try:
        model = load_model('best_fish_model_v4.h5', compile=False)  # Disable compilation if custom loss was used
        scaler = joblib.load('scaler_v4.pkl')
        mse = MeanSquaredError()
        model.compile(optimizer='adam', loss=mse)
    except Exception as e:
        print(f"{__name__}: {e}")
        # app.logger.info(f"{__name__}: {e}")
    print("Model Loaded")


def predict_severity(longitude, latitude):
    global model, scaler
    prediction = None

    try:
        input_data = np.array([[longitude, latitude]])
        input_data_scaled = scaler.transform(input_data)  # Scale input data
        prediction = model.predict(input_data_scaled)
    except Exception as e:
        print(f"{__name__}: {e}")
        # app.logger.info(f"{__name__}: {e}")

    return prediction


def predict_severity_matrix(longitude, latitude):
    dist_delta = 32 * 0.0145
    start_long = longitude - dist_delta * (SQUARE_MILES / 2)
    start_lat = latitude + dist_delta * (SQUARE_MILES / 2)
    severity_matrix = np.zeros((SQUARE_MILES, SQUARE_MILES))

    for long in range(SQUARE_MILES):
        for lat in range(SQUARE_MILES):
            new_long = start_long + long * dist_delta
            new_lat = start_lat + lat * dist_delta

            severity_matrix[long, lat] = severity_score(predict_severity(new_long, new_lat))

    return severity_matrix


def severity_score(arr):
    transformed_arr = np.square(arr * 100) / 2000
    weighted_average = np.sum(transformed_arr) / 10
    sigmoid_value = 1 / (1 + np.exp(-weighted_average * 10))

    return round((min(sigmoid_value - 0.5, 0.5) / 0.5), 2)


def print_summary(latitude: float, longitude: float):
    severity_scores = predict_severity(latitude, longitude)
    total_score = severity_score(severity_scores)

    predictions_with_species = list(zip(fish_species, severity_scores[0].tolist()))
    sorted_predictions = sorted(predictions_with_species, key=lambda x: x[1], reverse=True)

    for species, score in sorted_predictions:
        print(f"{species}: {score:.2f}")

    print(f"Resulting severity score: {total_score}")


# print_summary(-100.0, 91.0)
