import requests
import json
import os
from datetime import datetime
import logging

os.makedirs("logs", exist_ok=True) 
logging.basicConfig(
    filename='logs/api.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  # Recommended for modern Python versions
)

def fetch_weather_data():
    url = ("https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&daily=sunrise&hourly=temperature_2m,soil_temperature_0cm&timezone=Asia%2FSingapore"
    )
    # url=("https://www.google.com/search?q=import+requests+import+json+import+os+from+datetime+import+datetime+import+logging+def+fetch_weather_data%28%29%3A+url+%3D+%28%22https%3A%2F%2Fapi.open-meteo.com%2Fv1%2Fforecast%3Flatitude%3D52.52%26longitude%3D13.41%26daily%3Dsunrise%26hourly%3Dtemperature_2m%2Csoil_temperature_0cm%26timezone%3DAsia%252FSingapore%22+%29+try%3A+response+%3D+requests.get%28url%29+response.raise_for_status%28%29+data+%3D+response.json%28%29+return+data+except+requests.RequestException+as+e%3A+logging.error%28f%22%7Bdatetime.now%28%29%7D+-+Error+fetching+weather+data%3A+%7Be%7D%22%29+return+None+def+save_to_bronze%28data%29%3A+%23+Make+sure+the+folder+exists+os.makedirs%28%22data%2Fbronze%22%2C+exist_ok%3DTrue%29+%23+File+name+example%3A+data%2Fbronze%2F22-01-2025.json+filename+%3D+datetime.now%28%29.strftime%28%22%25d-%25m-%25Y.json%22%29+filepath+%3D+os.path.join%28%22data%2Fbronze%22%2C+filename%29+with+open%28filepath%2C+%22w%22%29+as+f%3A+json.dump%28data%2C+f%2C+indent%3D2%29+print%28f%22%5BOK%5D+Raw+weather+saved+%7Bfilepath%7D%22%29+def+main%28%29%3A+print%28%22Fetching+weather+data...%22%29+weather+%3D+fetch_weather_data%28%29+if+weather%3A+save_to_bronze%28weather%29+else%3A+print%28%22%E2%9D%8C+No+data+received.+Check+logs+for+details.%22%29+if+__name__+%3D%3D+%22__main__%22%3A+main%28%29+explain+this+code+step+by+step&sourceid=chrome&ie=UTF-8&amc=1&gs_lcrp=EgZjaHJvbWUyBggAEEUYOdIBCjI3MzI3ajBqMzOoAgawAgE&oq=import+requests+import+json+import+os+from+datetime+import+datetime+import+logging+def+fetch_weather_data%28%29%3A+url+%3D+%28%22https%3A%2F%2Fapi.open-meteo.com%2Fv1%2Fforecast%3Flatitude%3D52.52%26longitude%3D13.41%26daily%3Dsunrise%26hourly%3Dtemperature_2m%2Csoil_temperature_0cm%26timezone%3DAsia%252FSingapore%22+%29+try%3A+response+%3D+requests.get%28url%29+response.raise_for_status%28%29+data+%3D+response.json%28%29+return+data+except+requests.RequestException+as+e%3A+logging.error%28f%22%7Bdatetime.now%28%29%7D+-+Error+fetching+weather+data%3A+%7Be%7D%22%29+return+None+def+save_to_bronze%28data%29%3A+%23+Make+sure+the+folder+exists+os.makedirs%28%22data%2Fbronze%22%2C+exist_ok%3DTrue%29+%23+File+name+example%3A+data%2Fbronze%2F22-01-2025.json+filename+%3D+datetime.now%28%29.strftime%28%22%25d-%25m-%25Y.json%22%29+filepath+%3D+os.path.join%28%22data%2Fbronze%22%2C+filename%29+with+open%28filepath%2C+%22w%22%29+as+f%3A+json.dump%28data%2C+f%2C+indent%3D2%29+print%28f%22%5BOK%5D+Raw+weather+saved+%7Bfilepath%7D%22%29+def+main%28%29%3A+print%28%22Fetching+weather+data...%22%29+weather+%3D+fetch_weather_data%28%29+if+weather%3A+save_to_bronze%28weather%29+else%3A+print%28%22%E2%9D%8C+No+data+received.+Check+logs+for+details.%22%29+if+__name__+%3D%3D+%22__main__%22%3A+main%28%29+++explain+this+code+step+by+step&aep=109&cud=0&qsubts=1776694336557&source=chrome.crn.obic&cs=1&hl=en-GB&biw=1536&bih=695.2000122070312&mstk=AUtExfAEcSdierFBBTUtH9BOxZDW0LHShEfUQBZ9Jcw0Rq7jDqh8narccg6Z7mHHNsmXYiDLYMb6LmKwdF5hIXB4fFGrlpMLmerlc_nqLFCcAqE9qoX3SI0nELt6r8Z68WhZyeuiicjWXDGSoG5v6wsEaDm1hiTj3OzY8Zkk1tMvLe4E88TXYIiY7WTEK5tCwDITUPfyn7gwIOOmhhlxAXQjJgqv8gnEgSGhPt7V6-ZJMbEfCf4frx6K17OiD-_q37eEkGFzkhrqMdsvPw&csuir=1&mtid=QzTmaYLuDYyaseMP5LXWmQg&udm=50")
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