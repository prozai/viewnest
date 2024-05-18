from datetime import date
from app import session 
from flask import session as flask_session
from app.entity.models import Property 
from flask import render_template, request, redirect, url_for, flash, jsonify
import os
from datetime import datetime
from app.entity.models import *

class viewPropertyController:
    
    # # Function to add sample properties.
    # def add_sample_properties():
    #     try:
    #         # Sample property creation
    #         listing_date1 = date(2024, 4, 4)
    #         property1 = Property("12 Woodlands Street 12", "HDB", "Woodlands", 3, 800000.00, 2938, listing_date1, None, "./static/uploads/properties/property1.jpg", False)
    #         listing_date2 = date(2024, 2, 13)
    #         date_sold2 = date(2024, 4, 3)
    #         property2 = Property("29 Tampines Street 41", "Condo", "Tampines", 3, 1200000.00, 1382, listing_date2, date_sold2, "./static/uploads/properties/property2.jpg", True)
            
    #         # Check if properties already exist before adding them
    #         existing_properties = session.query(Property).filter(Property.propertyname.in_(["12 Woodlands Street 12", "29 Tampines Street 41"])).all()

    #         if not existing_properties:
    #             session.add_all([property1, property2])
    #             session.commit()
    #             print("Sample properties added successfully.")
    #         else:
    #             print("Sample properties already exist.")
    #     except Exception as e:
    #         session.rollback()
    #         print(f"Error adding sample properties: {e}")
    #     finally:
    #         session.close()

    # Function to show all properties.
    def view_properties(offset, limit, filter_type):
        properties = Property.view_properties(offset, limit, filter_type)
        return properties 
    
    # Function to show selected property.
    def view_property_detail(property_id):
        property = Property.view_property_detail(property_id)
        user_id = flask_session['user_id']
        is_saved = Save.is_saved(user_id, property_id)
        if is_saved:
            property.is_saved = True
        else:
            property.is_saved = False

        return property

    def load_more_properties(offset, limit, filter_type):
        try:
            properties = Property.load_more_properties(offset, limit, filter_type)
            if not properties:
                return jsonify(error="No properties found"), 404
            return jsonify(properties=properties)
        except Exception as e:
            print("Error loading more properties:", str(e))
            return jsonify(error="Internal server error"), 500
    
class viewCountController:
    # Function to add view count to property when viewed.
    def add_viewCount(property_id):
        try:
            property = Property.add_ViewCount(property_id)
            return property
        except Exception as e:
            print(f"Error fetching property: {e}")
            return None

# Create Property Listing
class createPropertyController:
    def REA_createProperty(self, propertyname, propertytype, district, bedroom_no, price, psf, image_file, selleremail):
        try:
            user_id = flask_session['user_id']
            max_id = Property.get_max_id(Property.ID)
            highest_id = max_id.ID if max_id else None

            propertyid = highest_id + 1
            filename = f"{propertyid}.{image_file.filename.split('.')[-1]}"
            upload_folder = './app/static/uploads/properties/'
            path = './static/uploads/properties/'
            image_file.save(os.path.join(upload_folder, filename))
            image_path = os.path.join(path, filename)

            new_property = Property(user_id=user_id,  # flask_session['user_id']
                                    propertyname=propertyname,
                                    propertytype=propertytype,
                                    district=district,
                                    bedroom_no=bedroom_no,
                                    price=price,
                                    psf=psf,
                                    selleremail=selleremail,
                                    listing_date=datetime.now().date(),
                                    date_sold=None,
                                    image_url= image_path,
                                    sold=False)
            
            Property.create_property(new_property)
        except Exception as e:
            print("Error creating property:", str(e))

# REA View Property Listings
class REAPropertiesController:
    def REA_viewProperties():
        try:
            user_id = flask_session['user_id']
            properties = Property.get_REAproperties(user_id)
            return properties

        except Exception as e:
            print("Error retrieving property listings:", str(e))

# Update Property Listing
class updatePropertyController:
    def REA_updateProperty(self, id, propertyname, propertytype, district, bedroom_no, price, psf, selleremail, image_file):
        try:
            updateProperty = Property.get_property_by_id(id)

            if updateProperty:
                updateProperty.propertyname = propertyname
                updateProperty.propertytype = propertytype
                updateProperty.district = district
                updateProperty.bedroom_no = bedroom_no
                updateProperty.price = price
                updateProperty.psf = psf
                updateProperty.selleremail = selleremail

                if image_file:
                    filename = f"{updateProperty.ID}.{image_file.filename.split('.')[-1]}"
                    upload_folder = './app/static/uploads/properties/'
                    path = './static/uploads/properties/'
                    image_file.save(os.path.join(upload_folder, filename))
                    image_path = os.path.join(path, filename)
                    updateProperty.image_url = image_path

                Property.update_property()
                return updateProperty
            else:
                return None

        except Exception as e:
            print("Error updating property:", str(e))
            return None

    def REA_getProperty(self, id):
        try:
            property = Property.get_property_by_id(id)
            return property
        except Exception as e:
            print("Error retrieving property:", str(e))

# Delete Property Listing
class deletePropertyController:
    def REA_deleteProperty(id):
        try:
            property = Property.get_property_by_id(id)
            if property:
                if property.image_url:
                    upload_folder = './app/static/uploads/properties/'
                    image_path = os.path.join(upload_folder, property.image_url.split("/")[-1])
                    if os.path.exists(image_path):
                        os.remove(image_path)

                Property.delete_property(property)
            else:
                print("Property not found", str(e))

        except Exception as e:
            print("Error deleting property:", str(e))

#Search
class SearchController:
    def search(self, search_query):
        if not search_query:
            return jsonify({'error': 'No query provided'}), 400

        results = Property.search_by_name(search_query)
        return results
    

    def searchSold(self, search_query):
        search_query = request.form.get('query')
        if not search_query:
            return jsonify({'error': 'No query provided'}), 400

        results = Property.search_by_sold(search_query)
        return results
    
    def searchAvailable(self, search_query):
        search_query = request.form.get('query')
        if not search_query:
            return jsonify({'error': 'No query provided'}), 400

        results = Property.search_by_avail(search_query)
        return results
    
    def searchPropertiesREA(self, search_query):
        search_query = request.form.get('query')
        user_id = flask_session['user_id']
        if not search_query:
            return jsonify({'error': 'No query provided'}), 400

        results = Property.search_by_REA_Properties(search_query,user_id)
        return results
    
search_controller = SearchController()

    
# Save property
class savePropertyController:
    def buyer_saveNewProperty():
        try:
            property_id = request.form['property_id']
            user_id = flask_session['user_id']
            saved = Save.get_save(user_id, property_id)
            property = Property.get_property_by_id(property_id)

            if saved:
                Save.delete_save_new(saved)
                Property.minus_save_new(property)
                return 'Save deleted'
            else:
                new_save = Save(user_id=user_id, property_id=property_id)
                Save.create_save_new(new_save)
                Property.add_save_new(property)
                return 'Save added'
        except Exception as e:
            print("Error adding saved property:", str(e))

    def buyer_saveSoldProperty():
            try:
                property_id = request.form['property_id']
                user_id = flask_session['user_id']
                saved = Save.get_save(user_id, property_id)
                property = Property.get_property_by_id(property_id)

                if saved:
                    Save.delete_save_sold(saved)
                    Property.minus_save_sold(property)
                    return 'Save deleted'
                else:
                    new_save = Save(user_id=user_id, property_id=property_id)
                    Save.create_save_sold(new_save)
                    Property.add_save_sold(property)
                    return 'Save added'
            except Exception as e:
                print("Error adding saved property:", str(e))

# Seller View Property Listings + Saves
class sellerPropertiesController:
    def seller_viewProperties():
        try:
            if 'email' in flask_session:
                    email = flask_session['email']            
                    properties = Property.get_sellerproperties(email)
                    return properties

        except Exception as e:
            print("Error retrieving property listings:", str(e))
