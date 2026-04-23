import json
import os
from datetime import datetime
import logging

# Configure logging to write to api.log
os.makedirs("logs", exist_ok=True) 
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  # Recommended for modern Python versions
)


def get_latest_bronze_file(bronze_folder="data/bronze"):
    """
    Finds the most recent JSON file in the bronze folder.
    """
    if not os.path.exists(bronze_folder):
        raise FileNotFoundError(f"Bronze folder not found: {bronze_folder}")
    files = [
        f for f in os.listdir(bronze_folder)
        if f.endswith(".json")
    ]
    if not files:
        raise FileNotFoundError("No JSON files found in bronze layer.")
    # Sort files by name; if you used date-based names this works well
    files.sort()
    latest_file = files[-1]
    return os.path.join(bronze_folder, latest_file)

def load_bronze_json(filepath):
    """
    Loads JSON data from the given bronze file path.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

def clean_weather(raw_json, city_name="Singapore"):
    """
    Transforms raw Open-Meteo JSON into a list of rows:
    [
      {"timestamp": "...", "temp": 1.2, "city": "Singapore"},
      ...
    ]
    """
    hourly = raw_json.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    soil_temps = hourly.get("soil_temperature_0cm", [])
   # Check for missing data
    if not times or not temps or not soil_temps:
        error_msg = "Missing 'time', 'temperature_2m', or 'soil_temperature_0cm' in JSON."
        logging.error(error_msg) # Records the error in api.log
        raise ValueError(error_msg)

# Check for length mismatch
    if len(times) != len(temps) or len(times) != len(soil_temps):
        error_msg = f"Length mismatch: times({len(times)}), temps({len(temps)}), soil({len(soil_temps)})"
        logging.error(error_msg)
        raise ValueError(error_msg)

    # If it reaches here, the data is valid
    logging.info(f"Data validation successful. Processed {len(times)} records.")
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

def save_to_silver(rows, silver_folder="data/silver"):
    """
    Saves the cleaned rows to a CSV file in the silver layer.
    File name example: data/silver/clean_2025-01-22.csv
    """
    os.makedirs(silver_folder, exist_ok=True)
    today_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"clean_{today_str}.csv"
    filepath = os.path.join(silver_folder, filename)
    # We will use the built-in csv module to keep it very "Python basics"
    import csv
    fieldnames = ["timestamp", "temp", "soil_temp", "city"]
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    logging.info(f"[OK] Cleaned data saved {filepath}")

def main():
    logging.info("Loading latest bronze file...")
    bronze_path = get_latest_bronze_file()
    logging.info(f"Using bronze file: {bronze_path}")
    raw_json = load_bronze_json(bronze_path)
    logging.info("Cleaning weather data into tabular format...")
    rows = clean_weather(raw_json, city_name="Singapore")
    logging.info(f"Total rows: {len(rows)}")
    logging.info("Saving to silver layer as CSV...")
    save_to_silver(rows)
    logging.info("Silver layer updated successfully.")

if __name__ == "__main__":
    main()

