from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_babel import _
from werkzeug.security import generate_password_hash
from app.control.adminController import RegisterProfile, RegisterAccount, showAllProfiles, showAllAccounts
from app.control.propertyController import ViewProperties,SearchController
from app.entity.models import User, UserProfile, Property
from app.control import bp
from app import session
from app.boundary.propertyBoundary import SearchPropertyBoundary

@bp.route('/')
def index():
    return render_template('index.html', title="")

@bp.route('/adminIndex')
def adminIndex():
    return render_template('systemAdmin/index.html', title="")

@bp.route('/allUsers', methods=["POST", "GET"])
def viewUsers():
    user_list = showAllAccounts()
    return render_template('systemAdmin/view-users.html', title="All Users", users=user_list)


@bp.route('/allProfiles', methods=["POST", "GET"])
def viewProfiles():
    profile_list = showAllProfiles()
    return render_template('systemAdmin/view-profiles.html', title="All Profile", profiles=profile_list)

@bp.route('/registerProfile', methods=['GET', 'POST'])
def addProfile():
    form = RegisterProfile()
    if form.validate_on_submit():
        user_profile = UserProfile(roles=form.role.data, description=form.description.data)
        UserProfile.create_new_profile(user_profile)
        flash('Profile created!')
        return redirect(url_for('.viewProfiles'))
    return render_template('systemAdmin/register-profile.html', title='Register Profile', form=form)

@bp.route('/registerAccount', methods=['GET', 'POST'])
def addAccount():
    form = RegisterAccount()
    if form.validate_on_submit():
        try:
            profile_name = form.profile_role.data
            profile=UserProfile.get_profile_by_name(name=profile_name)
            profile_id = profile.profile_id
            password_hash = generate_password_hash(password=form.password.data)
            user = User(profile_id=profile_id, 
                        fname=form.fname.data, 
                        lname=form.lname.data, 
                        email=form.email.data, 
                        phonenum=form.phonenum.data, 
                        username=form.username.data, 
                        password_hash=password_hash)
            User.create_new_account(user)
            flash('Account created!')
            return redirect(url_for('.viewUsers'))
        except Exception as e:
            print(e)
    return render_template('systemAdmin/register-account.html', title='Register Account', form=form)

