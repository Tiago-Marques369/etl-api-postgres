# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretório para dados
RUN mkdir -p data

# Variáveis de ambiente padrão (podem ser sobrescritas)
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DB_NAME=crypto_db
ENV DB_USER=tiagomarquespereira
ENV DB_PASS=

# Comando padrão
CMD ["python", "etl.py"]