FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY *.py ./

RUN mkdir -p resultados

EXPOSE 80

CMD ["python3", "servidorSequencial.py"]