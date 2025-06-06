from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

def get_db():
    conn = sqlite3.connect('data/oil_drift.db')
    return conn

class SensorData(BaseModel):
    temperatura: float
    umidade: float

@app.post("/sensor")
def receive_sensor(data: SensorData):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO sensor_data (temperatura, umidade) VALUES (?, ?)",
        (data.temperatura, data.umidade)
    )
    conn.commit()
    conn.close()
    return {"status": "ok"} 