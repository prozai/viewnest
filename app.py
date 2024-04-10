from flask import Flask, request, redirect, render_template, session
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "password"  # Change this to a random secret key

Base = declarative_base()

class SystemAdmin(Base):
    __tablename__ = "SystemAdmin"
    
    ID = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)  # Hash the password

engine = create_engine("sqlite:///viewnest.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
db_session = Session()

# Sample admin creation
admin = SystemAdmin("admin", "password")
db_session.add(admin)
db_session.commit()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db_session.query(SystemAdmin).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.ID
            return redirect('/dashboard')
        else:
            return 'Invalid username or password'
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = db_session.query(SystemAdmin).filter_by(ID=session['user_id']).first()
        if user:
            return f'Welcome, {user.username}!'
    return redirect('/login')

# Add a logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
