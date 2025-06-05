import requests
import sqlite3
import os
import dotenv
from datetime import datetime

dotenv.load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/oil_drift.db")
RAW_PATH = "data/raw/oil_slicks.json"

# Exemplo de função para buscar dados da API Cerulean (ajuste a URL e params conforme necessário)
def fetch_oil_slicks():
    # url = "https://api.cerulean.skytruth.org/oil_slicks"  # Exemplo
    # resp = requests.get(url)
    # resp.raise_for_status()
    # data = resp.json()
    # Para teste, use um exemplo mock:
    data = [{
        "id": "slick_001",
        "timestamp": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "lat": -18.161066,
        "lng": -37.919682,
        "area": 1.2,
        "confidence": 0.95
    }]
    return data

def save_raw(data):
    os.makedirs(os.path.dirname(RAW_PATH), exist_ok=True)
    import json
    with open(RAW_PATH, "w") as f:
        json.dump(data, f, indent=2)

def insert_oil_slick(conn, slick):
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO oil_slicks (id, timestamp, lat, lng, area, confidence)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (slick["id"], slick["timestamp"], slick["lat"], slick["lng"], slick["area"], slick["confidence"]))
    conn.commit()

def main():
    data = fetch_oil_slicks()
    save_raw(data)
    conn = sqlite3.connect(DB_PATH)
    for slick in data:
        insert_oil_slick(conn, slick)
    conn.close()
    print(f"{len(data)} manchas de óleo inseridas e salvas em {RAW_PATH}")

if __name__ == "__main__":
    main()
