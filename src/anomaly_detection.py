from sklearn.ensemble import IsolationForest
import pandas as pd
import os

# Paths to processed data
flight_data_path = 'data/processed/processed_flight_data.csv'
weather_data_path = 'data/processed/processed_weather_data.csv'
flight_anomalies_path = 'data/processed/flight_anomalies.csv'
weather_anomalies_path = 'data/processed/weather_anomalies.csv'

def detect_flight_anomalies():
    """Detect anomalies in flight velocity, altitude, and speed."""
    try:
        flight_df = pd.read_csv(flight_data_path)
        print("✅ Flight data loaded successfully!")

        # Debugging: Print available columns
        print("Flight Data Columns:", flight_df.columns.tolist())

        # Select multiple flight parameters
        features = ['velocity', 'geo_altitude', 'vertical_rate']

        # Ensure all required columns exist
        missing_features = [col for col in features if col not in flight_df.columns]
        if missing_features:
            print(f"❌ ERROR: Missing columns in flight data: {missing_features}")
            return

        # Apply Isolation Forest for anomaly detection
        model = IsolationForest(contamination=0.02, random_state=42)  # Reduced contamination rate
        flight_df['anomaly'] = model.fit_predict(flight_df[features])

        # 🛠 **Remove duplicate anomalies (same aircraft, same anomaly type)**
        anomalies = flight_df[flight_df['anomaly'] == -1]
        anomalies_before = len(anomalies)
        anomalies = anomalies.drop_duplicates(subset=['icao24', 'anomaly'])
        anomalies_after = len(anomalies)

        print(f"✅ Removed {anomalies_before - anomalies_after} duplicate flight anomalies, remaining anomalies: {anomalies_after}")

        # Save anomalies
        anomalies.to_csv(flight_anomalies_path, index=False)
        print(f"✅ Flight anomalies detected and saved! Total anomalies: {len(anomalies)}")

    except FileNotFoundError:
        print("❌ ERROR: Flight data file not found. Run `data_processor.py` first.")

def detect_weather_anomalies():
    """Detect anomalies in weather data using Isolation Forest."""
    try:
        weather_df = pd.read_csv(weather_data_path)
        print("✅ Weather data loaded successfully!")

        # Debugging: Print available column names
        print("Weather Data Columns:", weather_df.columns.tolist())

        # Rename 'main.temp' to 'temperature' if needed
        if 'main.temp' in weather_df.columns:
            weather_df.rename(columns={'main.temp': 'temperature'}, inplace=True)

        # 🛠 **Remove duplicate weather entries (same city, same timestamp)**
        before_count = len(weather_df)
        weather_df = weather_df.drop_duplicates(subset=['city', 'timestamp'])
        after_count = len(weather_df)
        print(f"✅ Removed {before_count - after_count} duplicate records, remaining records: {after_count}")

        # Select multiple weather parameters (only those available)
        available_features = ['temperature', 'humidity', 'pressure', 'wind_speed']
        features = [col for col in available_features if col in weather_df.columns]

        # Ensure we have enough features for model training
        if len(features) < 3:
            print(f"❌ ERROR: Not enough valid features in weather data. Found: {features}")
            return

        # Apply Isolation Forest for anomaly detection
        model = IsolationForest(contamination=0.02, random_state=42)  # Reduced contamination rate
        weather_df['anomaly'] = model.fit_predict(weather_df[features])

        # 🛠 **Remove duplicate anomalies (same city, same anomaly type)**
        anomalies = weather_df[weather_df['anomaly'] == -1]
        anomalies_before = len(anomalies)
        anomalies = anomalies.drop_duplicates(subset=['city', 'anomaly'])
        anomalies_after = len(anomalies)

        print(f"✅ Removed {anomalies_before - anomalies_after} duplicate weather anomalies, remaining anomalies: {anomalies_after}")

        # Save cleaned anomalies
        anomalies.to_csv(weather_anomalies_path, index=False)
        print(f"✅ Weather anomalies detected and saved! Total anomalies: {len(anomalies)}")

    except FileNotFoundError:
        print("❌ ERROR: Weather data file not found. Run `data_processor.py` first.")

if __name__ == "__main__":
    detect_flight_anomalies()
    detect_weather_anomalies()
