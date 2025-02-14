import requests
import pandas as pd 
import os
from datetime import datetime
import time

# Replace with your OpenWeatherMap API key
API_KEY = "65f80e26f766467a4675103ba9921f6a"

# Full list of U.S. cities for weather data collection
CITIES = [
    "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
    "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
    "Austin", "Jacksonville", "Fort Worth", "Columbus", "San Francisco",
    "Charlotte", "Indianapolis", "Seattle", "Denver", "Washington D.C.",
    "Boston", "El Paso", "Nashville", "Detroit", "Oklahoma City",
    "Portland", "Las Vegas", "Memphis", "Louisville", "Baltimore",
    "Milwaukee", "Albuquerque", "Tucson", "Fresno", "Sacramento",
    "Mesa", "Kansas City", "Atlanta", "Omaha", "Miami"
]

# Function to collect and store weather data
def collect_weather_data():
    all_data = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    for city in CITIES:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            city_data = {
                "city": city,
                "timestamp": timestamp,
                "temperature": data.get("main", {}).get("temp"),
                "humidity": data.get("main", {}).get("humidity"),
                "pressure": data.get("main", {}).get("pressure"),
                "wind_speed": data.get("wind", {}).get("speed"),
                "weather_main": data.get("weather", [{}])[0].get("main"),
                "weather_description": data.get("weather", [{}])[0].get("description")
            }
            all_data.append(city_data)
        else:
            print(f"❌ Failed to fetch data for {city} (Status Code: {response.status_code})")

    # Ensure the 'data/raw' folder exists
    os.makedirs('data/raw', exist_ok=True)

    # Convert data to DataFrame and Append to CSV
    df = pd.DataFrame(all_data)
    file_path = 'data/raw/weather_data.csv'

    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)  # Append data
    else:
        df.to_csv(file_path, mode='w', header=True, index=False)  # Create file and write data

    print(f"✅ Weather data collected for {len(all_data)} cities at {timestamp}")

# Run the script every 5 minutes
if __name__ == "__main__":
    while True:
        collect_weather_data()
        time.sleep(300)  # Collect data every 5 minutes
