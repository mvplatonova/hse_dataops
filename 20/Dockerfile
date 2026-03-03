FROM python:3.11-slim

LABEL maintainer=""
LABEL description="MLFlow tracking server"
LABEL version="1.0"

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /mlflow

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /mlflow/artifacts /mlflow/data

EXPOSE 5000

CMD ["mlflow", "server", \
     "--host", "0.0.0.0", \
     "--port", "5000"]
