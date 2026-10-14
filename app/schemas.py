from pydantic import BaseModel, Field, field_validator

class PredictionInput(BaseModel):
    edad: int = Field(..., ge=18, le=100, description="Edad biológica del usuario solicitante", example=35)
    ingresos: float = Field(..., ge=0.0, description="Ingresos anuales netos declarados", example=30000.0)
    num_transacciones: int = Field(..., ge=0, description="Volumen total de transacciones históricas", example=120)

    @field_validator('edad')
    @classmethod
    def validar_limite_edad(cls, value: int) -> int:
        if value < 18 or value > 100:
            raise ValueError("La edad proporcionada se encuentra fuera de los límites operativos autorizados (18-100).")
        return value

class PredictionOutput(BaseModel):
    prediccion: int = Field(..., description="Clase binaria asignada por el modelo (0 o 1)")
    probabilidad: float = Field(..., description="Probabilidad matemática de pertenencia a la clase positiva")
    status: str = Field("SUCCESS", description="Estado operativo de la inferencia ejecutada")