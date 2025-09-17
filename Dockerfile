FROM python:3.11-slim

# Setear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY main.py .
COPY ./app ./app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

