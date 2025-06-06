import sqlite3
import os
import dotenv

dotenv.load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/oil_drift.db")

def clear_weather_data():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM weather_data")
        print("Todos os dados da tabela weather_data foram apagados.")

if __name__ == "__main__":
    clear_weather_data() 