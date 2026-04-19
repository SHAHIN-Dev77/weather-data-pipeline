import requests
import json
import os
from datetime import datetime
import logging

def fetch_weather_data():
    url = ("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=sunrise&hourly=temperature_2m,soil_temperature_0cm&timezone=Asia%2FSingapore"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        logging.error(f"{datetime.now()} - Error fetching weather data: {e}")
    return None

def save_to_bronze(data):
    # Make sure the folder exists
    os.makedirs("data/bronze", exist_ok=True)
    # File name example: data/bronze/22-01-2025.json
    filename = datetime.now().strftime("%d-%m-%Y.json")
    filepath = os.path.join("data/bronze", filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[OK] Raw weather saved {filepath}")

def main():
    print("Fetching weather data...")
    weather = fetch_weather_data()
    if weather:
        save_to_bronze(weather)
    else:
        print("❌ No data received. Check logs for details.")
if __name__ == "__main__":
    main()