from werkzeug.security import generate_password_hash, check_password_hash
from entity.models import db, User

def create_user(username, password):
    user = User(username=username)
    user.password_hash = generate_password_hash(password)
    db.session.add(user)
    db.session.commit()
    return user

def verify_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return True
    return False
