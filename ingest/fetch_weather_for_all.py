import os
import sqlite3
import logging
from datetime import datetime, timedelta, timezone
import requests
import dotenv
from dateutil import parser as dtparser

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

dotenv.load_dotenv()

STORM_API_KEY = "5f4ece44-4279-11f0-9ea7-0242ac130006-5f4ece9e-4279-11f0-9ea7-0242ac130006"
DB_PATH = os.getenv("DB_PATH", "data/oil_drift.db")

WEATHER_PARAMS = [
    "windSpeed", "windDirection", "currentSpeed", "currentDirection", "waveHeight", "waterTemperature"
]


def fetch_weather(lat, lng, start_ts, end_ts):
    url = "https://api.stormglass.io/v2/weather/point"
    params = {
        "lat": lat,
        "lng": lng,
        "params": ",".join(WEATHER_PARAMS),
        "start": start_ts,
        "end": end_ts
    }
    headers = {"Authorization": STORM_API_KEY}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def extract_weather_values(escolhido):
    # Vento
    wind_speed = None
    for val in (escolhido.get("windSpeed") or {}).values():
        if val is not None:
            wind_speed = val
            break
    wind_dir = None
    for val in (escolhido.get("windDirection") or {}).values():
        if val is not None:
            wind_dir = val
            break
    # Corrente
    current_speed = None
    for val in (escolhido.get("currentSpeed") or {}).values():
        if val is not None:
            current_speed = val
            break
    current_dir = None
    for val in (escolhido.get("currentDirection") or {}).values():
        if val is not None:
            current_dir = val
            break
    # Onda
    wave_height = None
    for val in (escolhido.get("waveHeight") or {}).values():
        if val is not None:
            wave_height = val
            break
    # Temperatura da água
    water_temp = None
    for val in (escolhido.get("waterTemperature") or {}).values():
        if val is not None:
            water_temp = val
            break
    return wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp


def insert_weather(conn, oil_slick_id, timestamp, wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp):
    with conn:
        conn.execute(
            """
            INSERT INTO weather_data (
                oil_slick_id, timestamp, wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (oil_slick_id, timestamp, wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp)
        )


def get_all_oil_slicks(conn):
    cur = conn.cursor()
    cur.execute("SELECT id, lat, lng, timestamp FROM oil_slicks")
    return cur.fetchall()


def clear_weather_data(conn):
    with conn:
        conn.execute("DELETE FROM weather_data")


def main():
    if not STORM_API_KEY:
        logging.error("STORM_API_KEY não definido no .env.")
        return
    with sqlite3.connect(DB_PATH) as conn:
        clear_weather_data(conn)
        slicks = get_all_oil_slicks(conn)
        logging.info(f"Encontrados {len(slicks)} oil slicks para processar.")
        for oil_slick_id, lat, lng, timestamp_iso in slicks:
            try:
                dt = dtparser.isoparse(timestamp_iso)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                start_ts = int((dt - timedelta(hours=1)).timestamp())
                end_ts = int(dt.timestamp())
                data = fetch_weather(lat, lng, start_ts, end_ts)
                if not data.get("hours"):
                    logging.warning(f"Sem dados de clima para slick {oil_slick_id}.")
                    continue
                registro_completo = None
                for hora in data["hours"]:
                    cs_sources = hora.get("currentSpeed", {}) or {}
                    cd_sources = hora.get("currentDirection", {}) or {}
                    has_cs = any(val is not None for val in cs_sources.values())
                    has_cd = any(val is not None for val in cd_sources.values())
                    if has_cs and has_cd:
                        registro_completo = hora
                        break
                if registro_completo:
                    escolhido = registro_completo
                else:
                    escolhido = data["hours"][-1]
                wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp = extract_weather_values(escolhido)
                insert_weather(conn, oil_slick_id, timestamp_iso, wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp)
                logging.info(f"Clima inserido para slick {oil_slick_id} em {timestamp_iso}.")
            except Exception as e:
                logging.error(f"Erro ao processar slick {oil_slick_id}: {e}")

if __name__ == "__main__":
    main() 