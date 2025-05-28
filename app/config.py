import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = (
        'mysql+pymysql://flask:flask@database/'
        'flask_docker'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
