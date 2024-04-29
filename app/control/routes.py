from flask import jsonify, render_template, flash, redirect, url_for, request, session
from flask_babel import _
from werkzeug.security import generate_password_hash
from app import session
from app.control.adminController import RegisterProfile, RegisterAccount, showAllProfiles, showAllAccounts
from app.entity.models import User, UserProfile
from app.entity.models import Property
from app.control import bp
import os
from datetime import datetime

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

# Create Property Listing
@bp.route('/create_property', methods=['GET', 'POST'])
def create_property():
    if request.method == 'POST':
        propertyname = request.form['propertyname']
        propertytype = request.form['propertytype']
        district = request.form['district']
        bedroom_no = request.form['bedroom_no']
        price = request.form['price']
        psf = request.form['psf']
        image_file = request.files['image_url']

        if image_file:
            new_property = Property(user_id=1,  # session['user_id']
                                    propertyname=propertyname,
                                    propertytype=propertytype,
                                    district=district,
                                    bedroom_no=bedroom_no,
                                    price=price,
                                    psf=psf,
                                    listing_date=datetime.now().date(),
                                    date_sold=None,
                                    image_url=None,
                                    sold=False)
            session.add(new_property)
            session.commit()
            
            propertyid = new_property.ID
            filename = f"{propertyid}.{image_file.filename.split('.')[-1]}"
            upload_folder = './app/static/uploads/properties/'
            path = './static/uploads/properties/'
            image_file.save(os.path.join(upload_folder, filename))
            image_path = os.path.join(path, filename)
            
            new_property.image_url = image_path
            session.commit()

        else:
            image_path = None

        return jsonify({'success': True})

    return render_template('REAgent/create_property.html')

# REA View Property Listings
@bp.route('/REA_properties')
def REA_properties():
    properties = session.query(Property).filter_by(user_id=1).all() # session['user_id']
    return render_template('REAgent/REA_properties.html', properties=properties)
