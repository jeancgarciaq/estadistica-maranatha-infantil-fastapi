# Usar una imagen oficial de Python ligera
FROM python:3.11-slim

# Evitar que Python genere archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Instalar dependencias del sistema necesarias (si las hubiera)
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Comando para iniciar la aplicación
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}