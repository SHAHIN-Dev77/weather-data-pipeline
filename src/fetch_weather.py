import requests
import json
import os
from datetime import datetime
from config_loader import load_config

from logger import get_logger
logger = get_logger(__name__)


config = load_config()
city = config["city"]
api_config = config["weather_api"]
paths_config = config["paths"]

def duild_api_url()-> str:
    base_url = api_config["base_url"]
    lat=api_config["latitude"]
    lon=api_config["longitude"]
    hourly_params= api_config["hourly_parameters"]
    url = f"{base_url}?latitude={lat}&longitude={lon}&hourly={','.join(hourly_params)}&timezone=Asia%2FSingapore"
    # url = ("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=sunrise&hourly=temperature_2m,soil_temperature_0cm&timezone=Asia%2FSingapore"
    #     .format(
    #         api_config["latitude"],
    #         api_config["longitude"],
    #         ",".join(api_config["hourly_parameters"]),
    #         city
    #     )
    # )
    return url
def fetch_weather_data():
    url = duild_api_url()
    timeout=api_config.get("timeout_seconds", 10)
    logger.info("Starting API call to Open-Meteo...")
    logger.info(f"Fetching weather data from Open-Meteo API: {url} with timeout {timeout}s")
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.RequestException as e:
        logger.error(f"{datetime.now()} - Error fetching weather data: {e}")
    return None

def save_to_bronze(data):
    # Make sure the folder exists
    os.makedirs(paths_config["bronze_dir"], exist_ok=True)
    # File name example: data/bronze/22-01-2025.json
    filename = datetime.now().strftime("%d-%m-%Y.json")
    filepath = os.path.join(paths_config["bronze_dir"], filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"[OK] Raw weather saved {filepath}")

def main():
    logger.info("Fetching weather data...")
    weather = fetch_weather_data()
    if weather:
        save_to_bronze(weather)
    else:
        logger.error("❌ No data received. Check logs for details.")
if __name__ == "__main__":
    main()