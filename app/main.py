from fastapi import FastAPI, HTTPException, status
from app.schemas import PredictionInput, PredictionOutput
from app.model import model_orchestrator
from contextlib import asynccontextmanager
import logging

# Configuración del sistema corporativo de trazabilidad y logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("ProductionAPI")

@asynccontextmanager
async def application_lifespan(app_instance: FastAPI):
    # Evento de inicialización atómica en el arranque del hardware
    try:
        model_orchestrator.load_model_artifact()
        logger.info("INFRAESTRUCTURA: Binario del modelo de Machine Learning montado con éxito en RAM.")
    except Exception as exc:
        logger.critical(f"FALLO CRÍTICO DE STARTUP: No se pudo instanciar el modelo: {str(exc)}")
        raise exc
    yield
    # Evento de apagado limpio del proceso servidor
    logger.info("INFRAESTRUCTURA: Liberando y limpiando recursos de la API REST.")

app = FastAPI(
    title="API de Predicción Corporativa - ML Clásico",
    version="1.0.0",
    description="Servicio de alto rendimiento para la evaluación automatizada mediante modelos serializados.",
    lifespan=application_lifespan
)

@app.get("/health", status_code=status.HTTP_200_OK, tags=["Monitoreo"])
def perform_health_check():
    is_active = model_orchestrator.model is not None
    return {
        "status": "healthy" if is_active else "unhealthy",
        "model_loaded": is_active
    }

@app.post("/predict", response_model=PredictionOutput, status_code=status.HTTP_200_OK, tags=["Inferencia"])
def predict(payload: PredictionInput):
    try:
        pred_class, pred_prob = model_orchestrator.execute_inference(payload)
        logger.info(f"INFERENCIA EXITOSA: Predicción={pred_class} | Probabilidad={pred_prob:.4f}")
        return PredictionOutput(prediccion=pred_class, probabilidad=pred_prob)
    except Exception as error:
        logger.error(f"ERROR OPERATIVO INTERNO: {str(error)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Fallo interno en el motor matemático de predicción: {str(error)}"
        )