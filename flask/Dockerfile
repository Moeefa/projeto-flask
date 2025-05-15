FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /var/www/flask_docker

# Copiar requirements.txt
COPY app/requirements.txt .

# Instalar dependências
RUN pip install -r requirements.txt

# Copiar a aplicação - a pasta app e o arquivo run.py
COPY app/ ./app/
COPY run.py .

ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 9000

# Usar o arquivo run.py para iniciar a aplicação
CMD ["python", "-B", "run.py"]