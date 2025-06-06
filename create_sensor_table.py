import sqlite3

conn = sqlite3.connect('data/oil_drift.db')
conn.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperatura REAL,
    umidade REAL
);
""")
conn.commit()
conn.close()
print("Tabela sensor_data criada (ou já existia).") 