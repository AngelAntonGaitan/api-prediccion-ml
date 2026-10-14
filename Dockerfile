FROM python:3.10-slim

# Bloqueo de variables de entorno para optimizar la ejecución de Python en capas aisladas
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

# Instalación de dependencias críticas del sistema si fuesen requeridas
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia aislada del manifiesto de librerías para explotar el almacenamiento en caché de Docker
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia integral de los módulos de software y binarios matemáticos estructurados
COPY ./app ./app
COPY ./models ./models

# Creación y asignación de un usuario de seguridad sin privilegios de root
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Comando de arranque optimizado utilizando 4 workers concurrentes bajo protocolo ASGI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
