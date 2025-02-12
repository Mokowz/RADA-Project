import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("baringo-data.csv", parse_dates=['time'])

# Select relevant features for clustering
features = ['temperature', 'humidity', 'dew_point', 'wind_speed', 'pressure', 'precipitation']
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df[features])

# Apply K-Means clustering (Divide into  4 regions)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
df['region_id'] = kmeans.fit_predict(scaled_data)

# View sample clustered data
print(df[['time', 'region_id', 'temperature', 'humidity', 'precipitation']].head())

# Save clustered data
df.to_csv("baringo_clustered_data.csv", index=False)
