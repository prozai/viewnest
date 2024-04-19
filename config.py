import os
from flask_sqlalchemy import SQLAlchemy


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'too-bad-you-cant-find-555'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///viewnest.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    