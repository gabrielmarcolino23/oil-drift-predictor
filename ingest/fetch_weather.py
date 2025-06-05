import requests
import sqlite3
import os
import dotenv
from datetime import datetime, timedelta
import sys

dotenv.load_dotenv()

STORM_API_KEY = os.getenv("STORM_API_KEY")
DB_PATH = os.getenv("DB_PATH", "data/oil_drift.db")

def fetch_weather(lat, lng, start_ts, end_ts):
    url = "https://api.stormglass.io/v2/weather/point"
    params = {
        "lat": lat,
        "lng": lng,
        "params": ",".join([
            "windSpeed", "windDirection", "currentSpeed", "currentDirection", "waveHeight", "waterTemperature"
        ]),
        "start": start_ts,
        "end": end_ts
    }
    headers = {"Authorization": STORM_API_KEY}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()

def insert_weather(conn, oil_slick_id, timestamp, wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather_data (
            oil_slick_id, timestamp, wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (oil_slick_id, timestamp, wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp))
    conn.commit()

def extract_weather_values(hour):
    def get_first_value(d):
        if not d:
            return None
        for v in d.values():
            if v is not None:
                return v
        return None
    wind_speed = get_first_value(hour.get("windSpeed", {}))
    wind_dir = get_first_value(hour.get("windDirection", {}))
    current_speed = get_first_value(hour.get("currentSpeed", {}))
    current_dir = get_first_value(hour.get("currentDirection", {}))
    wave_height = get_first_value(hour.get("waveHeight", {}))
    water_temp = get_first_value(hour.get("waterTemperature", {}))
    return wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp

def main(oil_slick_id, lat, lng, timestamp_iso):
    dt = datetime.fromisoformat(timestamp_iso.replace("Z", "+00:00"))
    start_ts = int((dt - timedelta(hours=1)).timestamp())
    end_ts = int(dt.timestamp())
    data = fetch_weather(lat, lng, start_ts, end_ts)
    if not data.get("hours"):
        print("Nenhum dado retornado em data['hours'].")
        return
    # Tenta pegar o registro mais próximo do timestamp
    escolhido = min(data["hours"], key=lambda h: abs(datetime.fromisoformat(h["time"].replace("Z", "+00:00")) - dt))
    wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp = extract_weather_values(escolhido)
    conn = sqlite3.connect(DB_PATH)
    insert_weather(conn, oil_slick_id, timestamp_iso, wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp)
    conn.close()
    print(f"Dados de clima inseridos para oil_slick_id={oil_slick_id} em {timestamp_iso}")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Uso: python fetch_weather.py <oil_slick_id> <lat> <lng> <timestamp_iso>")
        sys.exit(1)
    oil_slick_id, lat, lng, timestamp_iso = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    main(oil_slick_id, lat, lng, timestamp_iso)
