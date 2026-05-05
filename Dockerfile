# Usamos una imagen ligera de Python 3.11
FROM python:3.11-slim

# Evita que Python genere archivos .pyc y permite que los logs se vean en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias para algunas librerías de Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiamos el archivo de requerimientos primero para aprovechar el cache de Docker
COPY requirements.txt .

# Instalamos las librerías de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el contenido del proyecto al contenedor
COPY . .

# Exponemos el puerto 8080 (puerto estándar para Google Cloud Run)
EXPOSE 8080

# Comando para iniciar la aplicación con Uvicorn
# Usamos 0.0.0.0 para que sea accesible externamente
CMD ["uvicorn", "main_web:app", "--host", "0.0.0.0", "--port", "8080"]