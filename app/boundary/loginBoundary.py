from flask import render_template, request, redirect, session, url_for
from app.control.loginController import loginController
from app.boundary import loginBP

class loginBoundary:
    @loginBP.route('/login', methods=['GET', 'POST'])
    def login():
        session.pop('user_id', None)
        session.pop('email', None)
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            result = loginController.login(username, password)
            if 'redirect' in result:
                return redirect(result['redirect'])
            error = result.get('error')
            return render_template('/login/login.html', error=error)
        return render_template('/login/login.html', error=None)

    @loginBP.route('/dashboard')
    def dashboard():
        result = loginController.dashboard()
        if 'redirect' in result:
            return redirect(result['redirect'])
        user = result.get('user')
        return render_template(result['template'], user=user)

    @loginBP.route('/logout', methods=['POST'])
    def logout():
        session.pop('user_id', None)
        session.pop('email', None)
        return redirect('/login')

# loginBoundary = loginBoundary()

# @loginBP.route('/login', methods=['GET', 'POST'])
# def login():    
#     return loginBoundary.login()

# @loginBP.route('/dashboard')
# def dashboard():
#     return loginBoundary.dashboard()

# @loginBP.route('/logout', methods=['POST'])
# def logout():
#     return loginBoundary.logout()

@loginBP.route('/login/access-denied')
def access_denied():
    return render_template('login/access-denied.html')
