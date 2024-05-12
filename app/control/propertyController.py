from datetime import date
from app import session 
from app.entity.models import Property 
from flask import render_template, request, redirect, url_for, flash
import os
from datetime import datetime
from app.entity.models import User

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
    def view_properties():
        try:
            properties = session.query(Property).all()
            return properties
        except Exception as e:
            print(f"Error fetching properties: {e}")
            return None
        finally:
            session.close()

    # Function to show selected property.
    def view_property_detail(property_id):
        try:
            property = session.query(Property).filter_by(ID=property_id).first()
            return property
        except Exception as e:
            print(f"Error fetching property: {e}")
            return None
        finally:
            session.close()

class viewCountController:
    # Function to add view count to property when viewed.
    def add_viewCount(property_id):
        try:
            property = session.query(Property).filter_by(ID=property_id).first()
            if property:
                property.view_count += 1
                session.commit()
                return property
        except Exception as e:
                session.rollback()
                print(f"Error fetching property: {e}")
                return None
        finally:
            session.close()

class createPropertyController:
    def REA_createProperty(user):
        try:

            if request.method == 'POST':
                user_id = request.form['user_id']
                propertyname = request.form['propertyname']
                propertytype = request.form['propertytype']
                district = request.form['district']
                bedroom_no = request.form['bedroom_no']
                price = request.form['price']
                psf = request.form['psf']
                image_file = request.files['image_url']
                selleremail = request.form['selleremail']

                if image_file:
                    new_property = Property(user_id=user_id,  # session['user_id']
                                            propertyname=propertyname,
                                            propertytype=propertytype,
                                            district=district,
                                            bedroom_no=bedroom_no,
                                            price=price,
                                            psf=psf,
                                            selleremail=selleremail,
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

                    flash("Added successfully!")

                else:
                    image_path = None

        except Exception as e:
            print("Error creating property:", str(e))


# REA View Property Listings
class viewPropertiesController:
    def REA_viewProperties(user):
        try:
            if 'user_id' in session:
                user_id = session['user_id']
                properties = session.query(Property).filter_by(user_id=user_id).all()
                return properties
            else:
                # Handle the case where user_id is not in session
                return "User ID not found in session."

        except Exception as e:
            print("Error retrieving property listings:", str(e))

# Update Property Listing
class updatePropertyController:
    def REA_updateProperty(self, id):
        try:
            if request.method == 'POST':
                propertyname = request.form['propertyname']
                propertytype = request.form['propertytype']
                district = request.form['district']
                bedroom_no = request.form['bedroom_no']
                price = request.form['price']
                psf = request.form['psf']
                image_file = request.files.get('image_url')

                updateProperty = session.query(Property).filter_by(ID=id).first()

                if updateProperty:
                    updateProperty.propertyname = propertyname
                    updateProperty.propertytype = propertytype
                    updateProperty.district = district
                    updateProperty.bedroom_no = bedroom_no
                    updateProperty.price = price
                    updateProperty.psf = psf
                    updateProperty.listing_date = datetime.now().date()

                    if image_file:
                        filename = f"{updateProperty.ID}.{image_file.filename.split('.')[-1]}"
                        upload_folder = './app/static/uploads/properties/'
                        path = './static/uploads/properties/'
                        image_file.save(os.path.join(upload_folder, filename))
                        image_path = os.path.join(path, filename)
                        updateProperty.image_url = image_path

                    session.commit()
                    flash("Updated successfully!")
                else:
                    flash("Property not found")

            property = session.query(Property).filter_by(ID=id).first()
            return property

        except Exception as e:
            print("Error updating property:", str(e))

# Delete Property Listing
class deletePropertyController:
    def REA_deleteProperty(self, id):
        try:
            property = session.query(Property).filter_by(ID=id).first()
            if property:
                # Remove the associated image file if it exists
                if property.image_url:
                    upload_folder = './app/static/uploads/properties/'
                    image_path = os.path.join(upload_folder, property.image_url.split("/")[-1])
                    if os.path.exists(image_path):
                        os.remove(image_path)

                session.delete(property)
                session.commit()
                flash("Deleted successfully!")
            else:
                flash("Property not found")

        except Exception as e:
            print("Error deleting property:", str(e))