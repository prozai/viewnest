from flask import render_template, redirect, url_for
from app.control.propertyController import *
from app.control import bp

class viewPropertyBoundary:
    def view_properties(self):
        viewPropertyController.add_sample_properties()
        properties = viewPropertyController.view_properties()
        return render_template('property/view_properties.html', properties=properties)

    def view_calculation(self):
        return render_template('property/view_calculation.html')

    def view_property_detail(self, property_id):
        property = viewPropertyController.view_property_detail(property_id)
        viewCountController.add_viewCount(property_id)
        return render_template('property/view_property_detail.html', property=property)

property_boundary = viewPropertyBoundary()
    
@bp.route('/view_properties')
def view_properties():
    return property_boundary.view_properties()
    
@bp.route('/view_calculation')
def view_calculation():
    return property_boundary.view_calculation()

@bp.route('/view_property_detail/<int:property_id>')
def view_property_detail(property_id):
    return property_boundary.view_property_detail(property_id)


class createPropertyPage():
    @bp.route('/create_property', methods=['GET', 'POST'])
    def create_property():
        if request.method == 'POST':
            try:
                propertyname = request.form.get("propertyname")
                propertytype = request.form.get("propertytype")
                district=request.form.get("district")
                bedroom_no=request.form.get("bedroom_no")
                price=request.form.get("price")
                psf=request.form.get("psf")
                image_file=request.files.get('image_url')
                selleremail=request.form.get("selleremail")

                newProperty = createPropertyController()
                property = newProperty.REA_createProperty(propertyname, propertytype, district, bedroom_no, price, psf, image_file, selleremail)

                if property:
                    return redirect(url_for('route.REA_view_properties'))
                else:
                    raise Exception('Error creating property')
            except Exception as e:
                print(e)
            flash("Added successfully!")
        return render_template('REAgent/create_property.html')
    
class REAPropertiesPage:
    @bp.route('/REA_properties')
    def REA_view_properties():
        properties = REAPropertiesController.REA_viewProperties()
        return render_template('REAgent/REA_properties.html', properties=properties)
    
class updatePropertyPage:
    @bp.route('/update_property/<int:id>/', methods=['GET', 'POST'])
    def update_property(id):
        property = None
        if request.method == 'POST':
            try:
                property = updatePropertyController.REA_updateProperty(id)
                if property:
                    flash("Updated successfully!")
                else:
                    flash("Property not found")
            except Exception as e:
                flash(f"Error updating property: {str(e)}")
            return redirect(url_for('route.update_property', id=id))
        
        property = updatePropertyController.REA_getProperty(id)
        return render_template('REAgent/update_property.html', property=property)
    
class deleteProperty:
    @bp.route('/delete_property/<int:id>/', methods=['POST'])
    def delete_property(id):
        try:
            delete = deletePropertyController.REA_deleteProperty(id)
        except Exception as e:
            flash("Error deleting property: " + str(e))
        
        flash("Deleted successfully!")
        return redirect(url_for('route.REA_view_properties'))

class saveProperty:
    @bp.route('/save_property', methods=['POST'])
    def save_property():
        savePropertyController.buyer_saveProperty()
        return redirect(url_for('route.view_properties'))

class sellerPropertiesPage:
    @bp.route('/seller_properties')
    def seller_view_properties():
        properties = sellerPropertiesController.seller_viewProperties()
        return render_template('property/seller_properties.html', properties=properties)
