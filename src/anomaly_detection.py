from sklearn.ensemble import IsolationForest
import pandas as pd
import os

def detect_flight_anomalies():
    flight_df = pd.read_csv('data/processed/processed_flight_data.csv')
    model = IsolationForest(contamination=0.05)
    flight_df['anomaly'] = model.fit_predict(flight_df[['velocity']])

    anomalies = flight_df[flight_df['anomaly'] == -1]
    anomalies.to_csv('data/processed/flight_anomalies.csv', index=False)
    print("Flight anomalies detected!")

def detect_weather_anomalies():
    weather_df = pd.read_csv('data/processed/processed_weather_data.csv')
    model = IsolationForest(contamination=0.1)
    weather_df['anomaly'] = model.fit_predict(weather_df[['main.temp']])

    anomalies = weather_df[weather_df['anomaly'] == -1]
    anomalies.to_csv('data/processed/weather_anomalies.csv', index=False)
    print("Weather anomalies detected!")

if __name__ == "__main__":
    detect_flight_anomalies()
    detect_weather_anomalies()
