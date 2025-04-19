import pandas as pd

# Load the original CSV
df = pd.read_csv("/home/ronny/rada-project/weather-data-csv/mandera_weather_data_2010_2020.csv")

# Select only the required columns
columns_to_keep = [
    "time", "temperature", "dew_point", "humidity",
    "wind_speed", "pressure", "precipitation"
]
df_filtered = df[columns_to_keep]

# Save to new CSV
df_filtered.to_csv("weather-data-csv/mandera-data.csv", index=False)
