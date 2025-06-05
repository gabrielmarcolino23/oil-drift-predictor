import streamlit as st
import pandas as pd
import sqlite3

def load_data(db_path="data/oil_drift.db"):
    conn = sqlite3.connect(db_path)
    df_oil = pd.read_sql_query("SELECT * FROM oil_slicks", conn)
    df_weather = pd.read_sql_query("SELECT * FROM weather_data", conn)
    conn.close()
    return df_oil, df_weather

def main():
    st.title("Oil Drift Predictor Dashboard")
    df_oil, df_weather = load_data()
    st.subheader("Manchas de Óleo Detectadas")
    st.dataframe(df_oil)
    st.subheader("Dados de Clima/Oceano")
    st.dataframe(df_weather)
    if not df_oil.empty:
        st.map(df_oil.rename(columns={"lat": "latitude", "lng": "longitude"}))

if __name__ == "__main__":
    main()
