import requests
import pandas as pd
from utils.config import OPENWEATHER_API_KEY

def fetch_pollution_data(lat, lon):

    url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return pd.DataFrame()

        data = response.json()

        if "list" not in data or not data["list"]:
            print("❌ No pollution data from API")
            return pd.DataFrame()

        pollution = data["list"][0]["components"]

        record = {
            "lat": lat,
            "lon": lon,
            "pm25": pollution.get("pm2_5", 0),
            "pm10": pollution.get("pm10", 0),
            "no2": pollution.get("no2", 0),
            "co": pollution.get("co", 0),
            "so2": pollution.get("so2", 0),   # ✅ ADDED
            "o3": pollution.get("o3", 0)
        }

        return pd.DataFrame([record])

    except Exception as e:
        print(f"❌ Exception occurred: {e}")
        return pd.DataFrame()