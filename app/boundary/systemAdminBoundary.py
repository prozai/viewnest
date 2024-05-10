from flask import render_template, redirect, url_for, request
from flask_babel import _
from app.control import adminBP
from app.control.adminController import ViewProfileController, ViewAccountController, CreateProfileController, CreateAccountController

@adminBP.route('/')
def index():
    return render_template('index.html', title="")

@adminBP.route('/adminIndex')
def adminIndex():
    return render_template('systemAdmin/index.html', title="")

# === User Profile ===

class CreateProfilePage():
    @adminBP.route('/registerProfile', methods=['GET', 'POST'])
    def createProfile():
        if request.method == "POST":
            try:
                role = request.form.get("role")
                description = request.form.get("description")
                user_profile = CreateProfileController()
                success = user_profile.addProfile(role, description)
                
                if success:
                    return redirect(url_for('.displayProfilePage'))
                else:
                    raise Exception ('Error in creating profile!')
            except Exception as e:
                print(e)
        return render_template('systemAdmin/register-profile.html')

class DisplayProfilesPage():
    @adminBP.route('/displayProfilesPage', methods=['POST', 'GET'])
    def displayProfile():
        view_profile = ViewProfileController()
        profile_list = view_profile.viewProfiles()
        return render_template('systemAdmin/view-profiles.html', title="All Profile", profiles=profile_list)

# === User Account ===

class DisplayAccountsPage():
    @adminBP.route('/displayAccountsPage', methods=['POST', 'GET'])
    def displayAccounts():
        view_accounts = ViewAccountController()
        user_list = view_accounts.viewUsers()
        return render_template('systemAdmin/view-users.html', title="All Users", users=user_list)

class CreateAccountsPage():
    @adminBP.route('/registerAccount', methods=['GET', 'POST'])
    def createAccount():
        if request.method == 'POST':
            try:
                profile_name = request.form.get("profile_role")
                password = request.form.get("password")
                fname=request.form.get("fname")
                lname=request.form.get("lname")
                email=request.form.get("email")
                phonenum=request.form.get("phonenum")
                username=request.form.get("username")

                add_account = CreateAccountController()
                status = add_account.addAccount(profile_name, fname, lname, email, phonenum, username, password)

                if status:
                    return redirect(url_for('.displayAccounts'))
                else:
                    raise Exception('Error in creating account!')
            except Exception as e:
                print("Error:", e)
        return render_template('systemAdmin/register-account.html')