import joblib
import numpy as np

def predict_position(timestamp, lat, lng, wind_speed, wind_dir, current_speed, current_dir, wave_height, water_temp):
    """
    Prediz a nova posição da mancha de óleo com base nos parâmetros ambientais.
    (Implementação de exemplo, substitua por modelo real depois)
    """
    # Exemplo: deslocamento simples pelo vetor de corrente
    import math
    delta_horas = 1  # previsão para 1 hora
    if current_speed is None or current_dir is None:
        return lat, lng  # sem corrente, sem deslocamento
    # Aproximação grosseira: 1 grau ~ 111km
    dist_km = current_speed * 3600 * delta_horas / 1000  # m/s para km
    delta_lat = dist_km * math.cos(math.radians(current_dir)) / 111
    delta_lng = dist_km * math.sin(math.radians(current_dir)) / (111 * math.cos(math.radians(lat)))
    return lat + delta_lat, lng + delta_lng

def predict_position_ml(lat, lng, current_speed, current_dir, horas, model_path="model/oil_drift_predictor.joblib"):
    """
    Prediz a nova posição da mancha de óleo usando o modelo treinado de ML.
    """
    model = joblib.load(model_path)
    X = np.array([[lat, lng, current_speed, current_dir, horas]])
    lat_pred, lng_pred = model.predict(X)[0]
    return lat_pred, lng_pred

# Exemplo de uso
if __name__ == "__main__":
    # Exemplo: prever posição para uma poça fictícia após 4 horas
    lat, lng = -20.0, -40.0
    current_speed, current_dir = 0.2, 120.0
    horas = 4
    lat_pred, lng_pred = predict_position_ml(lat, lng, current_speed, current_dir, horas)
    print(f"Posição prevista após {horas}h: lat={lat_pred:.5f}, lng={lng_pred:.5f}")
