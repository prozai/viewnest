from flask import render_template, redirect, url_for, request
from werkzeug.security import generate_password_hash
from flask_babel import _
from app.entity.models import User, UserProfile
from app.boundary import adminBP

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
    def updateProfile(self, role, role_name, description):
        status = UserProfile.update_profile(role, role_name, description)
        return status

# Suspend Profile Controller
class SuspendProfileController():
    def suspendProfile(self, role):
        status = UserProfile.suspend_profile(role)
        return status

# Search Profile Controller
class SearchProfileController():
    def searchProfile(self, search_term):
        results = UserProfile.searchProfile(search_term)
        return results

        
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
    
    def check_email(self, email):
        return User.check_email(email)
    
    def check_phonenum(self, phonenum):
        return User.check_phonenum(phonenum)
    
    def check_username(self, username):
        return User.check_username(username)


# View Account Controller
class ViewAccountController():
    def viewUsers(self):
        user_list = User.get_all_accounts()
        return user_list
    
# Update Account Controller
class UpdateAccountController():
 def getExistingAccount(self, username):
        user = User.get_account_by_username(username)
        return user

def updateAccount(self, username, fname, lname, email, phonenum, password):
  password_hash = generate_password_hash(password)
  status = User.update_account(username, fname, lname, email, phonenum, password_hash)
  return status

def check_email(self, email):
  return User.check_email(email)

def check_phonenum(self, phonenum):
  return User.check_phonenum(phonenum)
# Suspend Account Controller
class SuspendAccountController():
    def suspendAccount(self, username):
        status = User.suspend_account(username)
        return status
    
# Search Account Controller
class SearchAccountController():
    def searchAccount(self, search_term):
        results = User.searchAccount(search_term)
        return results