import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import joblib

# Carregar o dataset sintético
DATA_PATH = "data/synthetic_oil_drift.csv"
df = pd.read_csv(DATA_PATH)

# Features e targets
X = df[["lat_inicial", "lng_inicial", "current_speed", "current_dir", "horas"]]
y = df[["lat_prevista", "lng_prevista"]]

# Split treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinar modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Avaliação
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"MSE de teste: {mse:.6f}")

# Salvar modelo
joblib.dump(model, "model/oil_drift_predictor.joblib")
print("Modelo salvo em model/oil_drift_predictor.joblib")
