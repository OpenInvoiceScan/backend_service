# Usa Python 3.12
FROM python:3.12.3-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y poppler-utils


# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]