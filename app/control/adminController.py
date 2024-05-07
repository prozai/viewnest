from flask import render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash
from flask_babel import _
from app.entity.models import User, UserProfile
from app.control import adminBP

'''
@adminBP.route('/')
def index():
    return render_template('index.html', title="")

@adminBP.route('/adminIndex')
def adminIndex():
    return render_template('systemAdmin/index.html', title="")
'''

# ---  User Profile --- 

# Create Profile Controller
class CreateProfileController():
    @adminBP.route('/registerProfile', methods=['GET', 'POST'])
    def addProfile():
        if request.method == "POST":
            try:
                role = request.form.get("role")
                description = request.form.get("description")
                user_profile = UserProfile(role, description)
                                           #request.method.role.data, description=request.method.description.data)
                UserProfile.create_new_profile(profile=user_profile)
                #UserProfile.create_new_profile(user_profile)
                return redirect(url_for('.viewProfiles'))
            except Exception as e:
                print(e)
        return render_template('systemAdmin/register-profile.html')
    
# View Profile Controller
class ViewProfileController():
    @adminBP.route('/allProfiles', methods=['POST', 'GET'])
    def viewProfiles():
        profile_list = UserProfile.get_all_profiles()
        return render_template('systemAdmin/view-profiles.html', title="All Profile", profiles=profile_list)
    
# Update Profile Controller
class UpdateProfileController():
    @adminBP.route('/updateProfile', methods=['POST', 'GET'])
    def updateProfile():
        if request.method == "POST":
            try:
                role = request.form.get("profile_role")
                role_name = request.form.get("role")
                description = request.form.get("description")

                UserProfile.update_profile(role, role_name, description)

                return redirect(url_for('.viewProfiles'))
            except Exception as e:
                print(e)
        return render_template('systemAdmin/update-profile.html')

# Suspend Profile Controller
class SuspendProfileController():
    @adminBP.route('/suspendProfile', methods=['POST', 'GET'])
    def suspendProfile():
        if request.method == "POST":
            try:
                role = request.form.get("role")
                UserProfile.suspend_profile(role)

                return redirect(url_for('.viewProfiles'))
            except Exception as e:
                print(e)
        return render_template('systemAdmin/suspend-profile.html')

# Search Profile Controller
'''class SearchProfileController():
    @adminBP.route('/searchProfile', methods=['POST', 'GET'])
    def searchProfile():
        if request.method == "GET":
            try:
                search_term = request.args.get('term')
                attribute = request.args.get('attribute')
                results = UserProfile.searchProfile(search_term, attribute)

                return render_template('search_results.html', results=results)
            except Exception as e:
                print(e)
        return render_template('systemAdmin/view-profiles.html)
'''
        
# ---  User Account --- 

# Create Account Controller
class CreateAccountController():
    @adminBP.route('/registerAccount', methods=['GET', 'POST'])
    def addAccount():
        if request.method == 'POST':
            try:
                profile_name = request.form.get("profile_role")
                print(profile_name)
                profile=UserProfile.get_profile_by_name(name=profile_name)
                profile_id = profile.profile_id
                password_hash = generate_password_hash(password=request.form.get("password"))
                user = User(profile_id=profile_id, 
                            fname=request.form.get("fname"), 
                            lname=request.form.get("lname"), 
                            email=request.form.get("email"), 
                            phonenum=request.form.get("phonenum"), 
                            username=request.form.get("username"), 
                            password_hash=password_hash)
                print()
                User.create_new_account(user)
                return redirect(url_for('.viewUsers'))
            except Exception as e:
                print("Error:", e)
        return render_template('systemAdmin/register-account.html')

# View Account Controller
class ViewAccountController():
    @adminBP.route('/allUsers', methods=['POST', 'GET'])
    def viewUsers():
        user_list = User.get_all_accounts()
        return render_template('systemAdmin/view-users.html', title="All Users", users=user_list)
    
# Update Account Controller
class UpdateAccountController():
    @adminBP.route('/updateAccount', methods=['POST', 'GET'])
    def updateAccount():
        if request.method == "POST":
            try:
                username = request.form.get("username") 
                password_hash = generate_password_hash(password=request.form.get("password"))
                fname=request.form.get("fname")
                lname=request.form.get("lname") 
                email=request.form.get("email") 
                phonenum=request.form.get("phonenum")
                
                User.update_account(username, fname, lname, email, phonenum, password_hash)

                return redirect(url_for('.viewUsers'))
            except Exception as e:
                print(e)
        return render_template('systemAdmin/update-account.html')

# Suspend Account Controller
class SuspendAccountController():
    @adminBP.route('/suspendAccount', methods=['POST', 'GET'])
    def suspendAccount():
        if request.method == "POST":
            try:
                username = request.form.get("username")
                User.suspend_account(username)

                return redirect(url_for('.viewUsers'))
            except Exception as e:
                print(e)
        return render_template('systemAdmin/suspend-account.html')
    
# Search Account Controller
