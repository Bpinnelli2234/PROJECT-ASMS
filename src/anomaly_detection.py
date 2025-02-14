from sklearn.ensemble import IsolationForest
import pandas as pd
import os

# Paths to processed data
flight_data_path = 'data/processed/processed_flight_data.csv'
weather_data_path = 'data/processed/processed_weather_data.csv'

def detect_flight_anomalies():
    """Detect anomalies in flight velocity using Isolation Forest."""
    try:
        flight_df = pd.read_csv(flight_data_path)
        print("✅ Flight data loaded successfully!")

        # Check if 'velocity' column exists
        if 'velocity' not in flight_df.columns:
            print("❌ ERROR: 'velocity' column is missing in flight data.")
            return

        # Apply Isolation Forest for anomaly detection
        model = IsolationForest(contamination=0.05, random_state=42)
        flight_df['anomaly'] = model.fit_predict(flight_df[['velocity']])

        # Save anomalies
        anomalies = flight_df[flight_df['anomaly'] == -1]
        anomalies.to_csv('data/processed/flight_anomalies.csv', index=False)
        print("✅ Flight anomalies detected and saved!")

    except FileNotFoundError:
        print("❌ ERROR: Flight data file not found. Run `data_processor.py` first.")

def detect_weather_anomalies():
    """Detect anomalies in temperature using Isolation Forest."""
    try:
        weather_df = pd.read_csv(weather_data_path)
        print("✅ Weather data loaded successfully!")

        # 🔹 Debugging: Print available column names
        print("Weather Data Columns:", weather_df.columns.tolist())

        # Rename 'main.temp' to 'temperature' if needed
        if 'main.temp' in weather_df.columns:
            weather_df.rename(columns={'main.temp': 'temperature'}, inplace=True)
        
        # Ensure 'temperature' column exists
        if 'temperature' not in weather_df.columns:
            print("❌ ERROR: 'temperature' column is missing in weather data.")
            return

        # Apply Isolation Forest for anomaly detection
        model = IsolationForest(contamination=0.1, random_state=42)
        weather_df['anomaly'] = model.fit_predict(weather_df[['temperature']])

        # Save anomalies
        anomalies = weather_df[weather_df['anomaly'] == -1]
        anomalies.to_csv('data/processed/weather_anomalies.csv', index=False)
        print("✅ Weather anomalies detected and saved!")

    except FileNotFoundError:
        print("❌ ERROR: Weather data file not found. Run `data_processor.py` first.")

if __name__ == "__main__":
    detect_flight_anomalies()
    detect_weather_anomalies()
