import requests
import sqlite3
import os
import dotenv
from datetime import datetime
from shapely.geometry import shape

dotenv.load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/oil_drift.db")

CERULEAN_URL = (
    "https://api.cerulean.skytruth.org/collections/public.slick_plus/items"
    "?limit=9"
    "&bbox=-75,-35,-25,10"
    "&sortby=slick_timestamp"
)

def fetch_oil_slicks():
    resp = requests.get(CERULEAN_URL)
    resp.raise_for_status()
    data = resp.json()
    slicks = []
    for feature in data.get("features", []):
        props = feature["properties"]
        geom = feature["geometry"]
        # Calcular centroide do polígono
        try:
            centroid = shape(geom).centroid
            lat, lng = centroid.y, centroid.x
        except Exception:
            lat, lng = None, None
        slick = {
            "id": props["id"],
            "timestamp": props["slick_timestamp"],
            "lat": lat,
            "lng": lng,
            "area": props.get("area"),
            "confidence": props.get("machine_confidence"),
        }
        slicks.append(slick)
    return slicks

def clear_oil_slicks(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM oil_slicks")
    conn.commit()

def insert_oil_slick(conn, slick):
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO oil_slicks (id, timestamp, lat, lng, area, confidence)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (slick["id"], slick["timestamp"], slick["lat"], slick["lng"], slick["area"], slick["confidence"]))
    conn.commit()

def main():
    conn = sqlite3.connect(DB_PATH)
    clear_oil_slicks(conn)
    data = fetch_oil_slicks()
    for slick in data:
        insert_oil_slick(conn, slick)
    conn.close()
    print(f"{len(data)} manchas de óleo inseridas no banco de dados.")

if __name__ == "__main__":
    main()
