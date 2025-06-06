import os
import sqlite3
import subprocess
from datetime import datetime

def init_db():
    db_path = os.getenv("DB_PATH", "data/oil_drift.db")
    if not os.path.exists(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        with open("database/init.sql") as f:
            sql = f.read()
        conn = sqlite3.connect(db_path)
        conn.executescript(sql)
        conn.close()
        print("Banco de dados inicializado.")
    else:
        print("Banco de dados já existe.")

def ingest_oil_slick(oil_slick_id, timestamp, lat, lng, area, confidence):
    db_path = os.getenv("DB_PATH", "data/oil_drift.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO oil_slicks (id, timestamp, lat, lng, area, confidence)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (oil_slick_id, timestamp, lat, lng, area, confidence))
    conn.commit()
    conn.close()
    print(f"Mancha de óleo inserida: {oil_slick_id}")

def ingest_weather(oil_slick_id, lat, lng, timestamp):
    # Chama o script de clima
    subprocess.run([
        "python", "ingest/fetch_weather_for_all.py", str(oil_slick_id), str(lat), str(lng), str(timestamp)
    ], check=True)

def main():
    init_db()
    # Exemplo de ingestão manual (substitua por leitura da API Cerulean depois)
    oil_slick_id = "slick_001"
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    lat, lng, area, confidence = -18.161066, -37.919682, 1.2, 0.95
    ingest_oil_slick(oil_slick_id, timestamp, lat, lng, area, confidence)
    ingest_weather(oil_slick_id, lat, lng, timestamp)
    print("Pipeline de ingestão executado com sucesso.")

if __name__ == "__main__":
    main()
