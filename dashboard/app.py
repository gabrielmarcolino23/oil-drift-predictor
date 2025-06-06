import streamlit as st
import pandas as pd
import sqlite3
import sys
import os
import plotly.express as px
import plotly.graph_objects as go
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
from predictor import predict_position_ml

def load_data(db_path="data/oil_drift.db"):
    conn = sqlite3.connect(db_path)
    # Fazer join para pegar apenas poças com dados de clima
    query = '''
        SELECT o.*, w.wind_speed, w.wind_dir, w.current_speed, w.current_dir, w.wave_height, w.water_temp, w.timestamp as weather_timestamp
        FROM oil_slicks o
        INNER JOIN weather_data w ON o.id = w.oil_slick_id
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def load_sensor_data(db_path="data/oil_drift.db"):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 20", conn)
    conn.close()
    return df

def main():
    st.title("Oil Drift Predictor Dashboard")
    df = load_data()
    st.subheader("Manchas de Óleo com Dados de Clima/Oceano")
    st.dataframe(df)
    if df.empty:
        st.warning("Nenhuma poça com dados de clima disponível.")
        return

    # Seleção de poça
    slick_ids = df['id'].tolist()
    selected_id = st.selectbox("Selecione uma poça para prever a deriva:", slick_ids)
    selected = df[df['id'] == selected_id].iloc[0]

    # Parâmetros para previsão
    lat, lng = selected['lat'], selected['lng']
    current_speed, current_dir = selected['current_speed'], selected['current_dir']
    horas_list = [2, 4, 6, 8]
    cores = ['blue', 'orange', 'green', 'red', 'purple']

    # Previsões
    preds = []
    for i, horas in enumerate(horas_list):
        lat_pred, lng_pred = predict_position_ml(lat, lng, current_speed, current_dir, horas)
        preds.append({
            'horas': horas,
            'lat_predita': lat_pred,
            'lng_predita': lng_pred,
            'cor': cores[i+1]  # cores[0] será a posição atual
        })
    preds_df = pd.DataFrame(preds)

    st.subheader("Previsão de posição futura (modelo ML)")
    st.dataframe(preds_df)

    # Mapa interativo com Plotly
    map_df = pd.DataFrame({
        'latitude': [lat] + preds_df['lat_predita'].tolist(),
        'longitude': [lng] + preds_df['lng_predita'].tolist(),
        'tipo': ['Atual'] + [f"+{h}h" for h in horas_list],
        'cor': [cores[0]] + preds_df['cor'].tolist()
    })

    fig = go.Figure()
    # Posição atual
    fig.add_trace(go.Scattermapbox(
        lat=[lat], lon=[lng],
        mode='markers+text',
        marker=dict(size=14, color=cores[0]),
        text=['Atual'], textposition="top right",
        name='Atual',
        hoverinfo='text',
        hovertext=[f"Atual<br>Lat: {lat:.5f}<br>Lng: {lng:.5f}"]
    ))
    # Previsões
    for i, row in preds_df.iterrows():
        fig.add_trace(go.Scattermapbox(
            lat=[row['lat_predita']], lon=[row['lng_predita']],
            mode='markers+text',
            marker=dict(size=12, color=row['cor']),
            text=[f"+{row['horas']}h"], textposition="top right",
            name=f"+{row['horas']}h",
            hoverinfo='text',
            hovertext=[f"+{row['horas']}h<br>Lat: {row['lat_predita']:.5f}<br>Lng: {row['lng_predita']:.5f}"]
        ))
    # Linha de trajetória
    fig.add_trace(go.Scattermapbox(
        lat=map_df['latitude'], lon=map_df['longitude'],
        mode='lines', line=dict(color='black', width=2),
        name='Trajetória Prevista',
        hoverinfo='skip'
    ))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox_zoom=5,
        mapbox_center={"lat": lat, "lon": lng},
        margin={"r":0,"t":0,"l":0,"b":0},
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)
    st.write("Legenda: Azul = posição atual, demais cores = previsão para +2h, +4h, +6h, +8h. Linha tracejada = trajetória prevista.")

    st.subheader("Leituras do Sensor (Simulado)")
    sensor_df = load_sensor_data()
    st.dataframe(sensor_df)

if __name__ == "__main__":
    main()
