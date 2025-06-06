# Oil Drift Predictor 🌊🛢️

Sistema de monitoramento inteligente que coleta dados de manchas de óleo via satélite e prevê sua dispersão com base em condições climáticas em tempo real.

## Componentes
- 📡 Ingestão de dados via API Cerulean e OpenWeatherMap
- 🧠 Modelo de IA para previsão de deslocamento
- 🗺️ Dashboard com mapa interativo
- 🧰 Integração com ESP32 (simulado) para alertas físicos e envio de dados de sensor

## Passo a passo para executar o sistema

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Inicialize o banco de dados:**
   ```bash
   python main.py
   ```

3. **Inicie a API FastAPI para receber dados do sensor:**
   ```bash
   uvicorn utils.sensor_api:app --reload --port 8000
   ```

4. **Simule o envio de dados do sensor (sem hardware):**
   ```bash
   python simulate_sensor.py
   ```
   Isso irá enviar dados de temperatura e umidade simulados para o backend a cada 10 segundos.

5. **Abra o dashboard para visualizar os dados:**
   ```bash
   streamlit run dashboard/app.py
   ```
   O dashboard mostrará as previsões de deriva e as últimas leituras do sensor simulado.

---

Se quiser usar um sensor físico real, basta substituir o script de simulação pelo código do ESP32.

## Como rodar o pipeline de ingestão

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure o arquivo `.env` com sua chave da API StormGlass:
   ```env
   STORM_API_KEY=SEU_TOKEN_AQUI
   # DB_PATH=database/oil_drift.db (opcional)
   ```
3. Execute o pipeline principal:
   ```bash
   python main.py
   ```

Isso irá criar o banco, inserir um exemplo de mancha de óleo e buscar o clima correspondente, salvando tudo no SQLite.

---

Consulte o README original para detalhes do fluxo completo e estrutura de pastas.

## Como rodar

```bash
# Clonar e instalar dependências
git clone https://github.com/sua-org/oil-drift-predictor.git
cd oil-drift-predictor
pip install -r requirements.txt
