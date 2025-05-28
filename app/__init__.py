from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'random_secret_key'

# Mudança importante: alterar a configuração para apontar para o serviço 'database' no Docker
app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://flask:flask@database/'
    'flask_docker'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from app import routes, models
