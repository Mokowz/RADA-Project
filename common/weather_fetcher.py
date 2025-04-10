import pandas as pd
import requests
import numpy as np
from datetime import datetime, timedelta

def fetch_weather_data():
    # Define the past 10 days
    end_date = datetime.today()
    start_date = end_date - timedelta(days=30)
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude=0.4667&longitude=35.9667&daily=temperature_2m_max,temperature_2m_min,temperature_2m_mean,precipitation_sum,wind_speed_10m_max,relative_humidity_2m_max,relative_humidity_2m_min,dew_point_2m_max,surface_pressure_max&timezone=Africa/Nairobi&start_date={start_date.date()}&end_date={end_date.date()}"

    response = requests.get(url)
    data = response.json()
    print(data)



    df = pd.DataFrame({
        "date": pd.date_range(start=start_date, periods=31),
        "temperature": data["daily"]["temperature_2m_mean"],
        "precipitation": data["daily"]["precipitation_sum"],
        "humidity": data["daily"]["relative_humidity_2m_max"],
        "wind_speed": data["daily"]["wind_speed_10m_max"],
        "dew_point": data["daily"]["dew_point_2m_max"],
        "pressure": (np.array(data["daily"]["surface_pressure_max"]) / 30),
    })
    
    return df