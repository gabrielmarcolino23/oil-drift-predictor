import sqlite3
import os
import dotenv

dotenv.load_dotenv()

DB_PATH = os.getenv("DB_PATH", "data/oil_drift.db")

def clear_oil_slicks():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("DELETE FROM oil_slicks")
        print("Todos os dados da tabela oil_slicks foram apagados.")

if __name__ == "__main__":
    clear_oil_slicks() 