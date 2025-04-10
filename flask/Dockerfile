FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /var/www/flask_docker

COPY ../app/requirements.txt /var/www/flask_docker/requirements.txt

RUN pip install -r requirements.txt

COPY ../app .

EXPOSE 9000

#CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=9000"]

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "3", "--reload", "app:app"]




