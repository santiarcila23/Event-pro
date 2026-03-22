FROM python:3.11-slim

# Dependencias del sistema para Tkinter y Pillow
RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libfontconfig1 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Código de la aplicación
COPY . .

# Crear carpetas necesarias
RUN mkdir -p exports assets

CMD ["python", "main.py"]
