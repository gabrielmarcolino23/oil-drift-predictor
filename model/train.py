import sqlite3
import pandas as pd

def load_data(db_path="data/oil_drift.db"):
    conn = sqlite3.connect(db_path)
    df_oil = pd.read_sql_query("SELECT * FROM oil_slicks", conn)
    df_weather = pd.read_sql_query("SELECT * FROM weather_data", conn)
    conn.close()
    return df_oil, df_weather

def main():
    df_oil, df_weather = load_data()
    print("Dados de manchas:", df_oil.head())
    print("Dados de clima:", df_weather.head())
    # Aqui você pode implementar o pipeline de feature engineering e modelagem
    # Exemplo: merge, preparar X/y, treinar modelo, salvar modelo

if __name__ == "__main__":
    main()
