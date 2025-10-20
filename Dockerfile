FROM python:3.9-slim

WORKDIR /app

COPY *.py ./

# Cria a pasta resultados
RUN mkdir -p resultados

# Instalar net-tools para debugging de rede
RUN apt-get update && apt-get install -y net-tools iputils-ping && rm -rf /var/lib/apt/lists/*

EXPOSE 80

# Não é bom definir CMD fixo aqui
# O docker-compose vai definir qual servidor rodar