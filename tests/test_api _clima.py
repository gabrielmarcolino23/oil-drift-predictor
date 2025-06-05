import requests
import sqlite3
from datetime import datetime, timedelta
import os
import dotenv
# Carrega as variáveis de ambiente do arquivo .env  
dotenv.load_dotenv()

# ============================================
# 1) Defina suas variáveis principais
# ============================================
STORM_API_KEY = os.getenv("STORM_API_KEY")
lat = -18.161066  # ponto costeiro de interesse
lng = -37.919682   # ponto costeiro de interesse

# ============================================
# 2) Defina o intervalo de tempo (start, end)
# ============================================
# Buscar dados nas últimas 24 horas para maximizar chance de ter corrente disponível
agora_utc = datetime.utcnow()
inicio_utc = agora_utc - timedelta(hours=24)

start_ts = int(inicio_utc.timestamp())
end_ts = int(agora_utc.timestamp())

# ============================================
# 3) Monte a URL e cabeçalho
# ============================================
url = "https://api.stormglass.io/v2/weather/point"
params = {
    "lat": lat,
    "lng": lng,
    "params": ",".join([
        "windSpeed",
        "windDirection",
        "currentSpeed",
        "currentDirection",
        "waveHeight",
        "waterTemperature"
    ]),
    "start": start_ts,
    "end": end_ts
}
headers = {
    "Authorization": STORM_API_KEY
}

# ============================================
# 4) Faça a requisição e trate possíveis erros
# ============================================
try:
    resposta = requests.get(url, params=params, headers=headers, timeout=10)
    resposta.raise_for_status()
    data = resposta.json()
except requests.exceptions.HTTPError as http_err:
    print("Falha HTTP ao acessar StormGlass:", http_err)
    raise SystemExit(1)
except requests.exceptions.RequestException as e:
    print("Outro erro de requisição:", e)
    raise SystemExit(1)

# ============================================
# 5) Encontre o primeiro registro horário com corrente disponível
# ============================================
if not data.get("hours"):
    print("Nenhum dado retornado em data['hours']. Confira seu intervalo ou local.")
    raise SystemExit(1)

registro_completo = None
for hora in data["hours"]:
    # verifica qualquer fonte em currentSpeed e currentDirection
    cs_sources = hora.get("currentSpeed", {}) or {}
    cd_sources = hora.get("currentDirection", {}) or {}
    # encontra se há algum valor não None em currentSpeed e currentDirection
    has_cs = any(val is not None for val in cs_sources.values())
    has_cd = any(val is not None for val in cd_sources.values())
    if has_cs and has_cd:
        registro_completo = hora
        break

if registro_completo:
    escolhido = registro_completo
    origem = "primeiro com corrente disponível"
else:
    # se não achar corrente, cai no último registro disponível
    escolhido = data["hours"][-1]
    origem = "último registro (sem corrente disponível)"

# 5.1) timestamp textual (ISO UTC)
timestamp = escolhido.get("time")

# 5.2) vento (windSpeed + windDirection)
wind_speed = None
wind_dir = None
for src, val in (escolhido.get("windSpeed") or {}).items():
    if val is not None:
        wind_speed = val
        break
for src, val in (escolhido.get("windDirection") or {}).items():
    if val is not None:
        wind_dir = val
        break

# 5.3) corrente (currentSpeed + currentDirection)
current_speed = None
current_dir = None
for src, val in (escolhido.get("currentSpeed") or {}).items():
    if val is not None:
        current_speed = val
        break
for src, val in (escolhido.get("currentDirection") or {}).items():
    if val is not None:
        current_dir = val
        break

# 5.4) onda (waveHeight)
wave_height = None
for src, val in (escolhido.get("waveHeight") or {}).items():
    if val is not None:
        wave_height = val
        break

# 5.5) temperatura da água (waterTemperature)
water_temp = None
for src, val in (escolhido.get("waterTemperature") or {}).items():
    if val is not None:
        water_temp = val
        break

# Imprime para conferência
print(f"Usando o {origem}:")
print("timestamp    :", timestamp)
print("wind_speed   :", wind_speed, "m/s")
print("wind_dir     :", wind_dir, "°")
print("current_speed:", current_speed, "m/s")
print("current_dir  :", current_dir, "°")
print("wave_height  :", wave_height, "m")
print("water_temp   :", water_temp, "°C")

# ============================================
print("✅ Dados extraidos com sucesso.")
