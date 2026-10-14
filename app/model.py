import joblib
import os
import numpy as np
from app.schemas import PredictionInput


class ModelManager:
    def __init__(self):
        self.model = None
        self.model_path = os.path.join(os.path.dirname(__file__), "../models/model.pkl")

    def load_model_artifact(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Error de Infraestructura: Binario no hallado en {self.model_path}")
        self.model = joblib.load(self.model_path)

    def execute_inference(self, data: PredictionInput) -> tuple:
        if self.model is None:
            raise RuntimeError("Error Operacional: El modelo no ha sido cargado explícitamente en el arranque.")

        # Transformación estructural a matriz bidimensional de tipo NumPy exigida por Scikit-Learn
        input_features = np.array([[
            data.edad,
            data.ingresos,
            data.num_transacciones
        ]])

        # Cómputo de predicción y probabilidades analíticas
        prediction_class = int(self.model.predict(input_features)[0])
        probabilities = self.model.predict_proba(input_features)[0]
        prediction_probability = float(probabilities[1]) if len(probabilities) > 1 else float(probabilities[0])

        return prediction_class, prediction_probability


model_orchestrator = ModelManager()
