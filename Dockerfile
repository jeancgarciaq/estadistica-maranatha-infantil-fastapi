# Usamos una imagen ligera de Python 3.12
FROM python:3.12-slim

# Evita que Python genere archivos .pyc y asegura que los logs se emitan sin buffer
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Directorio de trabajo en el contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias para algunas librerías de Python (como bcrypt o reportlab)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos e instalamos los requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código de la aplicación
COPY . .

# Exponemos el puerto que usa Cloud Run (8080 por defecto)
EXPOSE 8080

# Comando para ejecutar la aplicación con Uvicorn
CMD ["sh", "-c", "uvicorn main_web:app --host 0.0.0.0 --port ${PORT}"]