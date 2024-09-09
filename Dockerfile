# Definindo a versão do Python como argumento
ARG PYTHON_VERSION=3.10-slim

# Base da imagem
FROM python:${PYTHON_VERSION}

# Variáveis de ambiente para otimizar o Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalação das dependências necessárias para o psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Criação e definição do diretório de trabalho
RUN mkdir -p /code
WORKDIR /code

# Copia o arquivo de dependências primeiro para aproveitar o cache do Docker
COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/

# Copia todo o código da aplicação para o container
COPY . /code

# Variável de ambiente da SECRET_KEY pode ser configurada no Fly.io em vez de estar aqui diretamente.
# No Fly.io, você pode usar 'fly secrets set SECRET_KEY=<your-secret-key>' para configurar.
# ENV SECRET_KEY "E5oRmoNxgrPYMHBtE4bneMyTzy1DWVpFAOZHsxpI3nGfUkdkQJ"

# Coleta os arquivos estáticos
RUN python manage.py collectstatic --noinput

# Expõe a porta 8000 para o servidor
EXPOSE 8000

# Define o comando para iniciar o Gunicorn (servidor WSGI)
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "siteconfig.wsgi"]
