import numpy as np
import pandas as pd
import random
import math

# Parâmetros do dataset
N_SAMPLES = 1000  # número de exemplos sintéticos
N_POÇAS = 10      # número de poças diferentes simuladas

# Limites geográficos (exemplo: costa brasileira)
LAT_MIN, LAT_MAX = -30, -10
LNG_MIN, LNG_MAX = -50, -30

# Limites físicos
CURRENT_SPEED_MIN, CURRENT_SPEED_MAX = 0.01, 1.0  # m/s
CURRENT_DIR_MIN, CURRENT_DIR_MAX = 0, 360         # graus

# Tempos futuros para prever (em horas)
TIMES = [2, 4, 6, 8]

# Função para calcular deslocamento

def deslocamento(lat, lng, speed, direction_deg, horas):
    distancia_m = speed * horas * 3600  # metros
    direction_rad = math.radians(direction_deg)
    dx = distancia_m * math.sin(direction_rad)
    dy = distancia_m * math.cos(direction_rad)
    delta_lat = dy / 111320
    delta_lng = dx / (111320 * math.cos(math.radians(lat)))
    return lat + delta_lat, lng + delta_lng

# Gerar dataset sintético
rows = []
for i in range(N_SAMPLES):
    id_poca = random.randint(1, N_POÇAS)
    lat0 = random.uniform(LAT_MIN, LAT_MAX)
    lng0 = random.uniform(LNG_MIN, LNG_MAX)
    speed = random.uniform(CURRENT_SPEED_MIN, CURRENT_SPEED_MAX)
    direction = random.uniform(CURRENT_DIR_MIN, CURRENT_DIR_MAX)
    for t in TIMES:
        # Adiciona ruído ao deslocamento
        lat_f, lng_f = deslocamento(lat0, lng0, speed, direction, t)
        lat_f += np.random.normal(0, 0.01)  # ruído ~1km
        lng_f += np.random.normal(0, 0.01)
        rows.append({
            'id_poca': id_poca,
            'lat_inicial': lat0,
            'lng_inicial': lng0,
            'current_speed': speed,
            'current_dir': direction,
            'horas': t,
            'lat_prevista': lat_f,
            'lng_prevista': lng_f
        })

# Salvar como CSV
synthetic_df = pd.DataFrame(rows)
synthetic_df.to_csv('data/synthetic_oil_drift.csv', index=False)
print('Dataset sintético salvo em data/synthetic_oil_drift.csv') 