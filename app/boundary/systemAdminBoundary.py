from flask import render_template, redirect, url_for, request
from flask_babel import _
from app.boundary import adminBP
from app.control.adminController import ViewProfileController, ViewAccountController, CreateProfileController, CreateAccountController, UpdateProfileController, UpdateAccountController, SuspendProfileController, SuspendAccountController

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
                    return redirect(url_for('.displayProfile'))
                else:
                    raise Exception ('Error in creating profile!')
            except Exception as e:
                print(e)
        return render_template('systemAdmin/register-profile.html')

class DisplayProfilesPage():
    @adminBP.route('/displayProfiles', methods=['POST', 'GET'])
    def displayProfile():
        view_profile = ViewProfileController()
        profile_list = view_profile.viewProfiles()
        return render_template('systemAdmin/view-profiles.html', title="All Profile", profiles=profile_list)

class UpdateProfilePage():
    @adminBP.route('/updateProfile', methods=['POST', 'GET'])
    def updateUserProfile():
        if request.method == "POST":
            try:
                role = request.form.get("profile_role")
                role_name = request.form.get("role")
                description = request.form.get("description")

                update_profile = UpdateProfileController()
                status = update_profile.updateProfile(role, role_name, description)

                if status:
                    return redirect(url_for('.displayProfile'))
            except Exception as e:
                print(e)
        return render_template('systemAdmin/update-profile.html')

class SuspendProfilePage():
    @adminBP.route('/suspendProfile', methods=['POST', 'GET'])
    def suspendUserProfile():
        if request.method == "POST":
            try:
                role = request.form.get("role")
                
                suspend_profile = SuspendProfileController()
                status = suspend_profile.suspendProfile(role)

                if status:
                    return redirect(url_for('.displayProfile'))
            except Exception as e:
                print(e)
        return render_template('systemAdmin/suspend-profile.html')


# === User Account ===

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
    
class DisplayAccountsPage():
    @adminBP.route('/displayAccounts', methods=['POST', 'GET'])
    def displayAccounts():
        view_accounts = ViewAccountController()
        user_list = view_accounts.viewUsers()
        return render_template('systemAdmin/view-users.html', title="All Users", users=user_list)
    
class UpdateAccountPage():
    @adminBP.route('/updateAccount', methods=['POST', 'GET'])
    def updateUserAccount():
        if request.method == "POST":
            try:
                username = request.form.get("username")
                password=request.form.get("password")
                fname=request.form.get("fname")
                lname=request.form.get("lname") 
                email=request.form.get("email") 
                phonenum=request.form.get("phonenum")
                
                update_account = UpdateAccountController()
                status = update_account.updateAccount(username, fname, lname, email, phonenum, password)

                if status:
                    return redirect(url_for('.displayAccounts'))
                else:
                    raise Exception('Error in updating account!')
            except Exception as e:
                print(e)
        return render_template('systemAdmin/update-account.html')

class SuspendAccountPage():
    @adminBP.route('/suspendAccount', methods=['POST', 'GET'])
    def suspendAccount():
        if request.method == "POST":
            try:
                username = request.form.get("username")

                suspend_account = SuspendAccountController()
                status = suspend_account.suspendAccount(username)

                if status:
                    return redirect(url_for('.displayAccounts'))
            except Exception as e:
                print(e)
        return render_template('systemAdmin/suspend-account.html')
