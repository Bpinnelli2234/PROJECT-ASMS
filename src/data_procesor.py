import pandas as pd
import os

def process_data():
    flight_data_path = 'data/raw/flight_data.csv'
    weather_data_path = 'data/raw/weather_data.csv'
    
    os.makedirs('data/processed', exist_ok=True)

    # Process Flight Data
    if os.path.exists(flight_data_path):
        flight_df = pd.read_csv(flight_data_path)
        # print(flight_df)
        # 🔹 Ensure column names are lowercase & spaces removed
        flight_df.columns = flight_df.columns.str.strip().str.lower()
        

        flight_df.columns = [
            "icao24", "callsign", "origin_country", "time_position", "last_contact",
            "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
            "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
            "spi", "position_source", "timestamp"
        ]
        print(flight_df.columns)
        # 🔹 Fix Chained Assignment Issue
        flight_df["velocity"] = flight_df["velocity"].fillna(0)


        # 🔹 Fix inconsistent column names
        # if 'velocity' in flight_df.columns:
        #     flight_df['velocity'].fillna(0, inplace=True)
        # if 'velocity' in flight_df.columns:
        # flight_df['9'] = flight_df['9'].fillna(0, inplace=True)
        # else:
            # print("❌ ERROR: 'velocity' column missing in flight data.")


        flight_df.to_csv('data/processed/processed_flight_data.csv', index=False)
        print("✅ Flight data processed successfully!")

    # Process Weather Data
    if os.path.exists(weather_data_path):
        weather_df = pd.read_csv(weather_data_path)
        weather_df.fillna(0, inplace=True)  # Replace missing values with 0
        weather_df.to_csv('data/processed/processed_weather_data.csv', index=False)
        print("✅ Weather data processed successfully!")

if __name__ == "__main__":
    process_data()
