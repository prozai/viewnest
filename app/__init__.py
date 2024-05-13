import os
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash
from config import Config

# Create SQLAlchemy engine and session
db_name = "viewnest.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, db_name)

Base = declarative_base()

engine = create_engine("sqlite:///"+ db_path)
Session = sessionmaker(bind=engine)
session = Session()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Database setup
    
    # Drop database (if exist)
    # Base.metadata.drop_all(engine)

    # # Create database tables
    from app.entity.models import User
    # Base.metadata.create_all(engine)

    # # Add known user types to UserProfile
    # buyer = UserProfile(roles='buyer')
    # session.add(buyer)
    # session.commit()

    # seller = UserProfile(roles='seller')
    # session.add(seller)
    # session.commit()

    # realEstateAgent = UserProfile(roles='real estate agent')
    # session.add(realEstateAgent)
    # session.commit()

    # admin = UserProfile(roles='system admin')
    # session.add(admin)
    # session.commit()

    # Register blueprint
    from app.boundary.loginBoundary import loginBP
    from app.boundary.propertyBoundary import propBP    
    from app.boundary.systemAdminBoundary import adminBP
  
    app.register_blueprint(loginBP)
    app.register_blueprint(propBP)
    app.register_blueprint(adminBP)
    # Close session on app teardown
    #@app.teardown_appcontext
    #def shutdown_session(exception=None):
    #    session.remove()

    return app

from app.entity import models
