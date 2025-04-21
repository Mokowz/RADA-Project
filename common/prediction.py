import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
from .weather_fetcher import fetch_weather_data
from common.alerts_emails import send_combined_alert_email
from datetime import datetime, timedelta
from celery import shared_task


FLOOD_THRESHOLD = 70
DROUGHT_THRESHOLD = 70

# Load models
flood_model = tf.keras.models.load_model('models/lstm_flood_model.keras')
drought_model = tf.keras.models.load_model('models/lstm_drought_model.keras')

flood_scaler = joblib.load('flood_scaler.pkl')
drought_scaler = joblib.load('drought_scaler.pkl')

kmeans = joblib.load("models/kmeans_model.pkl")

# Input features
features = ['temperature', 'dew_point', 'humidity', 'wind_speed', 'pressure', 'precipitation']
sequence_length = 20
num_future_days = 7


def predict_flood():
    import tensorflow as tf
    import joblib

    print("FETCH WEATHER DATA FOR FLOOD HAS BEGUN\n")
    df = fetch_weather_data()

    flood_model = tf.keras.models.load_model('models/lstm_flood_model.keras')
    flood_scaler = joblib.load('flood_scaler.pkl')
    kmeans = joblib.load("models/kmeans_model.pkl")

    # Cluster the data
    df["region_id"] = kmeans.predict(df[features])

    print(df)

    print("FETCH WEATHER DATA AND CLUSTERING FOR FLOOD HAS COMPLETED\n")

    # Store original date column before transformation
    date_col = df["date"].copy()

    # Normalize the data
    scaled_df = flood_scaler.transform(df[features])

    # Prepare input sequences (starting from the most recent data)
    X_inputs = []
    forecast_dates = []

    # Start from the last `sequence_length` days (from 2025-04-10)
    start_index = len(df) - sequence_length  # This ensures we are starting from the most recent data
    seq = scaled_df[start_index:]  # Take the last `sequence_length` days

    # Add this sequence to the inputs
    X_inputs.append(seq)
    forecast_dates.append(date_col.iloc[-1])  # The last date in the dataset (2025-04-10)

    X_inputs = np.array(X_inputs)

    # Prepare for 7 day predictions
    results = []
    for i in range(num_future_days):  # 7 days ahead
        # Predict the next day (flood probability)
        print("FLOOD PREDICTION HAS BEGUN\n")

        predictions = flood_model.predict(X_inputs)
        flood_prob = round(float(predictions[0][0]) * 100, 2)  # Convert to percentage
        
        print("FLOOD PREDICTION HAS COMPLETED\n")

        # Store prediction for the current day
        results.append({
            "date": (forecast_dates[0] + timedelta(days=i)).date().isoformat(),
            "flood_probability": flood_prob
        })

        # Reshape the prediction to match the sequence dimensions for the next prediction
        # Add the predicted value (scaled) to the sequence
        new_input = np.append(X_inputs[0][-1, 1:], flood_prob / 100).reshape(1, 1, -1)  # Reshape to (1, 1, num_features)
        X_inputs = np.append(X_inputs, new_input, axis=1)  # Append to sequence
        X_inputs = X_inputs[:, 1:, :]  # Keep the sequence length fixed to `sequence_length`


    return results


def predict_drought():
    import tensorflow as tf
    import joblib

    print("FETCH WEATHER DATA FOR DROUGHT HAS BEGUN\n")

    df = fetch_weather_data()

    drought_model = tf.keras.models.load_model('models/lstm_drought_model.keras')
    drought_scaler = joblib.load('drought_scaler.pkl')
    kmeans = joblib.load("models/kmeans_model.pkl")

    # Cluster the data
    df["region_id"] = kmeans.predict(df[features])

    print(df)
    print("FETCH WEATHER DATA AND CLUSTERING FOR DROUGHT HAS COMPLETED\n")


    # Store original date column before transformation
    date_col = df["date"].copy()

    # Normalize the data
    scaled_df = drought_scaler.transform(df[features])

    # Prepare input sequences (starting from the most recent data)
    X_inputs = []
    forecast_dates = []

    # Start from the last `sequence_length` days (from 2025-04-10)
    start_index = len(df) - sequence_length  # This ensures we are starting from the most recent data
    seq = scaled_df[start_index:]  # Take the last `sequence_length` days

    # Add this sequence to the inputs
    X_inputs.append(seq)
    forecast_dates.append(date_col.iloc[-1])  # The last date in the dataset (2025-04-10)

    X_inputs = np.array(X_inputs)

    # Prepare for 7 day predictions
    results = []
    for i in range(num_future_days):  # 7 days ahead
        # Predict the next day (drought probability)
        predictions = drought_model.predict(X_inputs)
        drought_prob = round(float(predictions[0][0]) * 100, 2)  # Convert to percentage

        # Store prediction for the current day
        results.append({
            # "date": str(forecast_dates[0] + timedelta(days=i)),
            "date": (forecast_dates[0] + timedelta(days=i)).date().isoformat(),
            "drought_probability": drought_prob
        })

        # Reshape the prediction to match the sequence dimensions for the next prediction
        # Add the predicted value (scaled) to the sequence
        new_input = np.append(X_inputs[0][-1, 1:], drought_prob / 100).reshape(1, 1, -1)  # Reshape to (1, 1, num_features)
        X_inputs = np.append(X_inputs, new_input, axis=1)  # Append to sequence
        X_inputs = X_inputs[:, 1:, :]  # Keep the sequence length fixed to `sequence_length`


    return results

@shared_task
def predict_all():
    from .models import Predictions

    print("Running PREDICTIONS...\n")
    flood_pred = predict_flood()
    drought_pred = predict_drought()

    print(f"Flood Predictions: {flood_pred}")
    print(f"Drought Predictions: {drought_pred}")

    for f, d in zip(flood_pred, drought_pred):
        date = f['date']
        flood = f['flood_probability']
        drought = d['drought_probability']

        Predictions.objects.update_or_create(
            date = date,
            defaults = {
                "flood_probability": flood,
                "drought_probability": drought,
            }
        )

    # Check flood risks above threshold
    flood_risks = [(item['date'], item['flood_probability']) for item in flood_pred if item['flood_probability'] > FLOOD_THRESHOLD]

    # Check drought risks above threshold
    drought_risks = [(item['date'], item['drought_probability']) for item in drought_pred if item['drought_probability'] > DROUGHT_THRESHOLD]

    if flood_risks or drought_risks:
        send_combined_alert_email(flood_risks, drought_risks)

    # return {"flood": flood_pred, "drought": drought_pred}
    return "\nPREDICTIONS COMPLETED\n"

@shared_task
def test_celery():
    print("✅ Celery is working!")
    return "Celery ran successfully"
