import requests
import pandas as pd
import os
from datetime import datetime
import time

# OpenSky API URL
API_URL = "https://opensky-network.org/api/states/all"

def collect_flight_data():
    response = requests.get(API_URL)

    if response.status_code == 200:
        flight_data = response.json()
        
        print("✅ API Response Keys:", flight_data.keys())  # Debug API response structure
        print(f"✅ Number of columns in API response: {len(flight_data['states'][0])}")  # Debug number of columns

        # Convert API response to DataFrame
        df = pd.DataFrame(flight_data["states"])

        # Update column names to match OpenSky API format (17 columns)
        df.columns = [
            "icao24", "callsign", "origin_country", "time_position", "last_contact",
            "longitude", "latitude", "baro_altitude", "on_ground", "velocity",
            "true_track", "vertical_rate", "sensors", "geo_altitude", "squawk",
            "spi", "position_source"
        ]

        # Add a timestamp for tracking
        df["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Ensure the data directory exists
        os.makedirs("data/raw", exist_ok=True)

        # Save the collected data (Append Mode)
        file_path = "data/raw/flight_data.csv"
        if os.path.exists(file_path):
            df.to_csv(file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(file_path, mode='w', header=True, index=False)

        print(f"✅ Flight data collected successfully at {df['timestamp'].iloc[-1]}!")

    else:
        print(f"❌ Failed to fetch flight data: {response.status_code}")

# Run this every 5 minutes
if __name__ == "__main__":
    while True:
        collect_flight_data()
        time.sleep(300)  # Collect data every 5 minutes
