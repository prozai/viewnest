from flask import render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash
from flask_babel import _
from app.entity.models import User, UserProfile
from app.control import adminBP

# ---  User Profile --- 

# Create Profile Controller
class CreateProfileController():
    def addProfile(self, role, description):
        user_profile = UserProfile(role, description)
        status = UserProfile.create_new_profile(profile=user_profile)
        return status
    
# View Profile Controller
class ViewProfileController():
    def viewProfiles(self):
        profile_list = UserProfile.get_all_profiles()
        return profile_list
    
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
    def addAccount(self, profile_name, fname, lname, email, phonenum, username, password):
        try:
            profile=UserProfile.get_profile_by_name(name=profile_name)
            profile_id = profile.profile_id
            password_hash = generate_password_hash(password)

            user = User(profile_id, fname, lname, email, phonenum, username, password_hash)
            User.create_new_account(user)

            return True
        except Exception as e:
            print("Error:", e) 
        return False

# View Account Controller
class ViewAccountController():
    def viewUsers(self):
        user_list = User.get_all_accounts()
        return user_list
    
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
