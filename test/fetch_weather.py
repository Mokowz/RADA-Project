import requests
import pandas as pd
from datetime import datetime, timedelta
import json
import numpy as np
import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

loaded_model = load_model("models/lstm_flood_model.h5")

def fetch_weather_data():
    # Define the past 10 days
    end_date = datetime.today()
    start_date = end_date - timedelta(days=10)
    print(f'Start Date: {start_date} \nEnd Date: {end_date}')

    url = f"https://api.open-meteo.com/v1/forecast?latitude=0.4667&longitude=35.9667&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min,dew_point_2m_max,surface_pressure_max&timezone=Africa/Nairobi&start_date={start_date.date()}&end_date={end_date.date()}"


    response = requests.get(url)
    data = response.json()
    print(data)


    with open('test/data.json', 'w') as f:
        json.dump(data, f)

    df = pd.DataFrame({
        "date": pd.date_range(start=start_date, periods=11),
        "temperature": data["daily"]["temperature_2m_mean"],
        "precipitation": data["daily"]["precipitation_sum"],
        "humidity": data["daily"]["relative_humidity_2m_max"],
        "wind_speed": data["daily"]["wind_speed_10m_max"],
        "dew_point": data["daily"]["dew_point_2m_max"],
        "pressure": (np.array(data["daily"]["surface_pressure_max"]) / 30),
    })
    
    return df

print("Hello There")
weather_data = fetch_weather_data()
print("Done")

# features = ['temperature', 'humidity', 'dew_point', 'wind_speed', 'pressure', 'precipitation']
features = ['temperature', 'dew_point', 'humidity', 'wind_speed', 'pressure', 'precipitation']

# Cluster the data
kmeans = joblib.load("models/kmeans_model.pkl")
weather_data["region_id"] = kmeans.predict(weather_data[features])


print(weather_data)


# Preprocess the data and scale it
scaler = joblib.load('flood_scaler.pkl')
weather_data_scaled = scaler.transform(weather_data[features])


sequence_length = 10  # The LSTM model was trained with 10-day sequences
num_future_days = 5   # We want predictions for the next 7 days

X_inputs = []

# Ensure sequence length is respected
for i in range(num_future_days):
    seq = weather_data_scaled[i:i+sequence_length]  # Slicing the NumPy array
    
    if seq.shape[0] == sequence_length:  # Only include full sequences
        X_inputs.append(seq)

print(f"X Inputs: {X_inputs}")
# Convert to a NumPy array properly
X_inputs = np.array(X_inputs)

# Make predictions for each sequence
predicted_probabilities = loaded_model.predict(X_inputs)

# Convert probabilities to percentage format
flood_probabilities = [round(float(prob[0]) * 100, 2) for prob in predicted_probabilities]

# Display results
for i, prob in enumerate(flood_probabilities):
    print(f"Flood Probability for Day {i+1}: {prob}%")
