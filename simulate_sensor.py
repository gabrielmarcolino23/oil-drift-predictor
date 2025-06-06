import requests
import random
import time

URL = "http://localhost:8000/sensor"

while True:
    temperatura = round(random.uniform(20.0, 30.0), 2)
    umidade = round(random.uniform(50.0, 100.0), 2)
    payload = {
        "temperatura": temperatura,
        "umidade": umidade
    }
    try:
        resp = requests.post(URL, json=payload)
        print(f"Enviado: {payload} | Resposta: {resp.status_code} {resp.text}")
    except Exception as e:
        print("Erro ao enviar:", e)
    time.sleep(10)  # envia a cada 10 segundos 