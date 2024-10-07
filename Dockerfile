# Use a imagem oficial do Python como base
FROM python:3.8-slim

# Define o diretório de trabalho
WORKDIR /projeto

# Instala gcc e outras dependências necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    python3-distutils \
    python3-setuptools \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos para a imagem
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o diretório de trabalho
COPY ./app /projeto/app
COPY ./dev.env /projeto/dev.env

# Expõe a porta que o FastAPI utilizará
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
