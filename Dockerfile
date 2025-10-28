FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Instalar Python e dependências INCLUINDO CURL
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    net-tools \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

WORKDIR /app

COPY . .

RUN pip install matplotlib numpy seaborn pandas

CMD ["python3", "servidorSequencial.py"]