from datetime import date
from app import session 
from app.control import bp
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_babel import _
from app.entity.models import User, UserProfile, Property

# Function to add sample properties. (to remove after integration)
def add_sample_properties():
    try:
        # Sample property creation
        listing_date1 = date(2024, 4, 4)
        property1 = Property("12 Woodlands Street 12", "HDB", "Woodlands", 3, 800000.00, 2938, listing_date1, None, "./static/uploads/properties/property1.jpg", False)
        listing_date2 = date(2024, 2, 13)
        date_sold2 = date(2024, 4, 3)
        property2 = Property("29 Tampines Street 41", "Condo", "Tampines", 3, 1200000.00, 1382, listing_date2, date_sold2, "./static/uploads/properties/property2.jpg", True)
        
        # Check if properties already exist before adding them
        existing_properties = session.query(Property).filter(Property.propertyname.in_(["12 Woodlands Street 12", "29 Tampines Street 41"])).all()

        if not existing_properties:
            session.add_all([property1, property2])
            session.commit()
            print("Sample properties added successfully.")
        else:
            print("Sample properties already exist.")
    except Exception as e:
        session.rollback()
        print(f"Error adding sample properties: {e}")
    finally:
        session.close()

# Function to show all properties.
class ViewProperties:
    def show_all_properties():
        try:
            properties = session.query(Property).all()
            return properties
        except Exception as e:
            print(f"Error fetching properties: {e}")
            return None
        finally:
            session.close()

@bp.route('/view_properties')
def view_properties():
    add_sample_properties()
    properties = ViewProperties.show_all_properties()
    return render_template('property/view_properties.html', properties=properties)

@bp.route('/view_calculation')
def view_calculation():
    return render_template('property/view_calculation.html')

#@bp.route('/search', methods=['POST' , 'GET'])
#def search():
    search_query = request.form.get('query')

    if not search_query:
        return jsonify({'error': 'No query provided'}), 400


    # Split the search query into individual keywords
    keywords = search_query.split()

    # Perform search using SQLAlchemy
    results = session.query(Property).filter(
        *[Property.propertyname.like(f'%{keyword}%') for keyword in keywords]
    ).all()

    # Close the session
    session.close()

    return render_template('property/search.html', results=results)

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
    
search_controller = SearchController()

    

