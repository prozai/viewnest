from flask import render_template, redirect, url_for, request
from flask_babel import _
from app.boundary import adminBP
from app.control.adminController import ViewProfileController, ViewAccountController, CreateProfileController, \
    CreateAccountController, UpdateProfileController, UpdateAccountController, SuspendProfileController, SuspendAccountController, \
    SearchProfileController, SearchAccountController

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
                status = update_profile.updateProfile(role, description)

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

class SearchProfilePage():
    @adminBP.route('/searchProfile', methods=['POST', 'GET'])
    def displaySearchProfile():
        try:
            search_term = request.form.get('query')
            search_profile = SearchProfileController()

            results = search_profile.searchProfile(search_term)

            if results :
                return render_template('systemAdmin/search_profile.html', results=results)
            else:
                print('None found!')
    
        except Exception as e:
            print(e)

        return render_template('systemAdmin/view-profiles.html')


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

                # Check if unique attributes exist
                if (add_account.check_email(email)):
                    return render_template('systemAdmin/register-account.html', error='Email already exists!')
                
                if (add_account.check_phonenum(phonenum)):
                    return render_template('systemAdmin/register-account.html', error='Phone number already exists!')
                
                if (add_account.check_username(username)):
                    return render_template('systemAdmin/register-account.html', error='Username already exists!')

                status = add_account.addAccount(profile_name, fname, lname, email, phonenum, username, password)

                if status:
                    return redirect(url_for('.displayAccounts'))
                else:
                    return redirect('systemAdmin/register-account.html', error='Error creating new account.')
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
    @adminBP.route('/edit/<string:username>', methods=['GET'])
    def edit_user(username):
        update_user = UpdateAccountController()
        user = update_user.getExistingAccount(username)
        if user:
            return render_template('systemAdmin/update-account.html', user=user, message="")
        else:
            return "User not found", 404

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
                temp = update_account.getExistingAccount(username)

                # Check if unique attributes exist
                if (update_account.check_email(email=email, username=username)):
                    return render_template('systemAdmin/update-account.html', user=temp, error='Email already exists!')
                
                if (update_account.check_phonenum(phonenum=phonenum, username=username)):
                    return render_template('systemAdmin/update-account.html', user=temp, error='Phone number already exists!')
                
                status = update_account.updateAccount(username, fname, lname, email, phonenum, password)

                if status:
                    message = "Update Successful!"

                    return render_template('systemAdmin/update-account.html', user=temp, message=message)
                else:
                    return render_template('systemAdmin/update-account.html', user=temp, error='Error updating account!')
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
                    return render_template('systemAdmin/suspend-account.html', message="Suspend Successful!")
                else:
                    return render_template('systemAdmin/suspend-account.html', Error='Error suspending account!')
            except Exception as e:
                print(e)
        return render_template('systemAdmin/suspend-account.html')
    
class SearchProfilePage():
    @adminBP.route('/searchAccount', methods=['POST', 'GET'])
    def displaySearchAccount():
        try:
            search_term = request.form.get('query')

            search_account = SearchAccountController()
            results = search_account.searchAccount(search_term)

            if results :
                return render_template('systemAdmin/search_account.html', results=results)
            else:
                print('None found!')
    
        except Exception as e:
            print(e)

        return render_template('systemAdmin/view-users.html')

