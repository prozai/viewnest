from datetime import date
from app import session 
from app.entity.models import Property 

# Function to add sample properties.
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
def show_all_properties():
    try:
        properties = session.query(Property).all()
        return properties
    except Exception as e:
        print(f"Error fetching properties: {e}")
        return None
    finally:
        session.close()
