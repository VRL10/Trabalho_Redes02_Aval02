FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY *.py ./

# Instalar net-tools para debugging de rede
RUN apt-get update && apt-get install -y net-tools iputils-ping && rm -rf /var/lib/apt/lists/*

EXPOSE 80

# O comando será sobrescrito no docker-compose
CMD ["python", "servidor_sequencial.py"]