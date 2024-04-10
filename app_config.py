class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///viewnest.db'
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_ADMIN_SWATCH = 'cerulean'  # A theme for Flask-Admin
