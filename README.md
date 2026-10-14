# 🚀 API de Predicción Corporativa (Machine Learning + FastAPI + Docker)

## 📌 Visión General
Este proyecto consiste en el desarrollo e implementación de un microservicio **RESTful** de alto rendimiento diseñado para exponer un modelo de **Machine Learning** (clasificación binaria con *scikit-learn*) como un servicio web accesible mediante el protocolo HTTP. 

El sistema garantiza el aislamiento de dependencias, validación estricta de datos en tiempo de ejecución, arquitectura limpia y contenedores inmutables listos para producción en la nube.

---

## 🛠️ Tecnologías Utilizadas

* **Python 3.10**: Lenguaje base para el desarrollo del backend y modelo.
* **FastAPI**: Framework web asíncrono de alto rendimiento para la construcción de la API REST.
* **Scikit-Learn & Joblib**: Algoritmo de clasificación (`RandomForestClassifier`) y serialización/carga del modelo en memoria.
* **Pydantic**: Validación estricta de esquemas y tipos de datos de entrada/salida.
* **Docker & Docker Compose**: Contenerización e inmunización del entorno de ejecución.
* **Uvicorn**: Servidor web ASGI para producción.

---

## 📐 Arquitectura del Sistema

El sistema sigue un patrón cliente-servidor strictly desacoplado con separación clara de responsabilidades:

* **Cliente**: Aplicación o sistema externo que envía solicitudes `POST` con datos JSON estructurados.
* **API Gateway (FastAPI)**: Punto de entrada que valida payloads con Pydantic y gestiona el enrutamiento.
* **Wrapper del Modelo (`ModelManager`)**: Carga el artefacto `.pkl` en RAM durante la fase de *startup* para minimizar latencias de I/O y ejecutar inferencias sobre matrices NumPy.
* **Contenedor Docker**: Unidad de aislamiento stateless para despliegue homogéneo.

---

## 📁 Estructura del Proyecto

```text
.
├── app/
│   ├── __init__.py           # Inicializador del paquete Python
│   ├── main.py               # Punto de entrada de FastAPI, enrutamiento y lifespan
│   ├── model.py              # Wrapper de inferencia para Scikit-Learn
│   └── schemas.py            # Modelos Pydantic para validación de contratos
├── models/
│   └── model.pkl             # Artefacto binario serializado del modelo ML
├── Dockerfile                # Imagen inmutable de producción
├── docker-compose.yml        # Orquestación de servicios y redes
├── Proyecto_API_de_Prediccion.pdf  # Documentación técnica oficial
└── requirements.txt          # Dependencias y versiones del proyecto
```

---

## 🔌 Contratos de la API REST

### 1. Health Check
* **Método**: `GET`
* **Ruta**: `/health`
* **Respuesta (`200 OK`)**:
  ```json
  {
    "status": "healthy",
    "model_loaded": true
  }
  ```

---

### 2. Endpoint de Inferencia
* **Método**: `POST`
* **Ruta**: `/predict`

#### 📥 Cuerpo de la petición (JSON Payload):
```json
{
  "edad": 35,
  "ingresos": 30000.0,
  "num_transacciones": 120
}
```

#### 📤 Respuesta (JSON Output):
```json
{
  "prediccion": 0,
  "probabilidad": 0.87,
  "status": "SUCCESS"
}
```

---

## ⚙️ Instalación y Ejecución Local

### Opción 1: Ejecución con Docker Compose (Recomendado)
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/AngelAntonGaitan/api-prediccion-ml.git
   cd api-prediccion-ml
   ```

2. **Levantar el contenedor**:
   ```bash
   docker-compose up --build
   ```

3. **Acceder a la documentación interactiva**:
   * OpenAPI (Swagger UI): `http://localhost:8000/docs`
   * ReDoc: `http://localhost:8000/redoc`

---

### Opción 2: Ejecución Entorno Local (Python)
1. **Crear y activar entorno virtual**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar el servidor Uvicorn**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

---

## 🧪 Buenas Prácticas y Escalabilidad

* **Desacoplamiento Total**: Separación estricta entre la lógica HTTP/API y el motor de inferencia matemática.
* **Fail-Fast**: Validación perimetral inmediata mediante Pydantic antes de consumir CPU en el modelo.
* **Carga Atómica en RAM**: Carga del binario `.pkl` únicamente al arrancar la aplicación (*lifespan*).
* **Preparado para Cloud & K8s**: Contenedor *stateless* diseñado para autoescalado horizontal (HPA) y balanceadores de carga.
