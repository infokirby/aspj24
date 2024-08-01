import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import joblib

data = pd.read_csv('login_data.csv')
data = pd.get_dummies(data, columns=['location'])

features = ['hour', 'day', 'month', 'year'] + [col for col in data.columns if col.startswith('location_SG')]
X = data[features].values


# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train the Isolation Forest model
iso_forest = IsolationForest(contamination=0.1, random_state=42)
iso_forest.fit(X_scaled)

# Save the model and the scaler
joblib.dump(iso_forest, 'iso_forest_model.pkl')
joblib.dump(scaler, 'scaler.pkl')