# Oil Drift Predictor 🌊🛢️

Sistema de monitoramento inteligente que coleta dados de manchas de óleo via satélite e prevê sua dispersão com base em condições climáticas em tempo real.

## Componentes
- 📡 Ingestão de dados via API Cerulean e API StormGlass
- 🧠 Modelo de IA para previsão de deslocamento
- 🗺️ Dashboard com mapa interativo
- 🧰 Integração com ESP32 (simulado) para alertas físicos e envio de dados de sensor

## Passo a passo para executar o sistema

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Inicialize o banco de dados (opcional, só se for criar do zero):**
   ```bash
   python main.py
   ```
   > **Atenção:** Rodar o main.py pode sobrescrever dados se o seu init.sql tiver comandos DROP TABLE. Use apenas se for iniciar do zero.

3. **Crie a tabela de sensores (sem afetar os dados existentes):**
   ```bash
   python create_sensor_table.py
   ```
   Isso garante que a tabela sensor_data existe no banco, sem apagar nada.

4. **Inicie a API FastAPI para receber dados do sensor:**
   ```bash
   uvicorn utils.sensor_api:app --reload --port 8000
   ```
   > Deixe esse terminal aberto enquanto simula o sensor.

5. **Simule o envio de dados do sensor (sem hardware):**
   ```bash
   python simulate_sensor.py
   ```
   Isso irá enviar dados de temperatura e umidade simulados para o backend a cada 10 segundos.
   > Se aparecer erro de conexão, verifique se a API FastAPI está rodando antes de executar o simulador.

6. **Abra o dashboard para visualizar os dados:**
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

## Como rodar

```bash
# Clonar e instalar dependências
git clone https://github.com/sua-org/oil-drift-predictor.git
cd oil-drift-predictor
pip install -r requirements.txt
