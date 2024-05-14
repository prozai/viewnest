from flask import render_template, request, redirect
from app.control.loginController import loginController
from app.boundary import loginBP

class loginBoundary:
    def login(self):
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            result = loginController.login(username, password)
            if 'redirect' in result:
                return redirect(result['redirect'])
            error = result.get('error')
            return render_template('/login/login.html', error=error)
        return render_template('/login/login.html', error=None)

    def dashboard(self):
        result = loginController.dashboard()
        if 'redirect' in result:
            return redirect(result['redirect'])
        user = result.get('user')
        return render_template(result['template'], user=user)

    def logout(self):
        result = loginController.logout()
        return redirect(result['redirect'])

loginBoundary = loginBoundary()

@loginBP.route('/login', methods=['GET', 'POST'])
def login():    
    return loginBoundary.login()

@loginBP.route('/dashboard')
def dashboard():
    return loginBoundary.dashboard()

@loginBP.route('/logout', methods=['POST'])
def logout():
    return loginBoundary.logout()

@loginBP.route('/login/access-denied')
def access_denied():
    return render_template('login/access-denied.html')