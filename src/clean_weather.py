import os
import json
from datetime import datetime
from src.logger import get_logger
logger = get_logger(__name__)

def get_latest_bronze_file(bronze_folder="data/bronze"):
    if not os.path.exists(bronze_folder):
        logger.error("Bronze folder not found")
        raise FileNotFoundError(f"Bronze folder not found: {bronze_folder}")
    files = [f for f in os.listdir(bronze_folder)
              if f.endswith(".json")
              ]
    if not files:
        logger.error("No bronze files found")
        raise FileNotFoundError(f"No bronze files found in {bronze_folder}")
    files.sort()
    latest_file = files[-1]
    return os.path.join(bronze_folder, latest_file)

def load_data(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

def clean_weather(raw_json, city_name="Singapore"):
    hourly = raw_json.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    soil_temps = hourly.get("soil_temperature_0cm", [])
    if not times or not temps or not soil_temps:
        logger.error("Missing 'time', 'temperature_2m', or 'soil_temperature_0cm' in JSON.")
        raise ValueError("Missing 'time', 'temperature_2m', or 'soil_temperature_0cm' in JSON.")
    if len(times) != len(temps) or len(times) != len(soil_temps):
        logger.error("Length mismatch between time, temperature, and soil lists.")
        raise ValueError("Length mismatch between time, temperature, and soil lists.")
    rows = []
    for t, temp, soil_temp in zip(times, temps, soil_temps):
        rows.append(
            {
                "timestamp": t,
                "temp": temp,
                "soil_temp": soil_temp,
                "city": city_name
            }
        )
    return rows