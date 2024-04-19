from app import create_app
from flask import Flask
from flask_login import LoginManager
from app.entity.models import User


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

@LoginManager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))