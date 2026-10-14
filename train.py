from sklearn.ensemble import RandomForestClassifier
import numpy as np
import joblib
import os

# Simulación de datos de entrenamiento históricos consolidados
X_train = np.array([[30, 50000, 100], [45, 80000, 250], [22, 15000, 10], [60, 120000, 400]])
y_train = np.array([0, 1, 0, 1])

# Instanciación del estimador con hiperparámetros bloqueados para reproducibilidad
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Persistencia en el sistema de archivos del proyecto
output_dir = "models"
os.makedirs(output_dir, exist_ok=True)
model_filename = os.path.join(output_dir, "model.pkl")
joblib.dump(model, model_filename)
print(f"Artefacto matemático serializado con éxito en: {model_filename}")