from flask import render_template, request, redirect, url_for
from app.control.propertyController import *
from app.control.loginController import loginController
from app.boundary import propBP

class viewPropertyBoundary:
    @propBP.route('/view_properties')
    @loginController.login_required
    def view_properties():
     #  viewPropertyController.add_sample_properties()
        properties = viewPropertyController.view_properties()
        return render_template('property/view_properties.html', properties=properties)

    def view_calculation():
        return render_template('property/view_calculation.html')

    def view_property_detail(self,property_id):
        property = viewPropertyController.view_property_detail(property_id)
        viewCountController.add_viewCount(property_id)
        return render_template('property/view_property_detail.html', property=property)
    
property_boundary = viewPropertyBoundary()


    
@propBP.route('/view_calculation')
@loginController.login_required
def view_calculation():
    return property_boundary.view_calculation()

@propBP.route('/view_property_detail/<int:property_id>')
@loginController.login_required
def view_property_detail(property_id):
    return property_boundary.view_property_detail(property_id)

class createPropertyPage():
    @propBP.route('/create_property', methods=['GET', 'POST'])
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
    @propBP.route('/REA_properties')
    def REA_view_properties():
        properties = REAPropertiesController.REA_viewProperties()
        return render_template('REAgent/REA_properties.html', properties=properties)
    
class updatePropertyPage:
    @propBP.route('/update_property/<int:id>/', methods=['GET', 'POST'])
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
            return redirect(url_for('propRoutes.update_property', id=id))
        
        property = updatePropertyController.REA_getProperty(id)
        return render_template('REAgent/update_property.html', property=property)
    
class deleteProperty:
    @propBP.route('/delete_property/<int:id>/', methods=['POST'])
    def delete_property(id):
        try:
            deletePropertyController.REA_deleteProperty(id)
        except Exception as e:
            flash("Error deleting property: " + str(e))
        
        flash("Deleted successfully!")
        return redirect(url_for('propRoutes.REA_view_properties'))

class saveProperty:
    @propBP.route('/save_property', methods=['POST'])
    def save_property():
        savePropertyController.buyer_saveProperty()
        return redirect(url_for('route.view_properties'))

class sellerPropertiesPage:
    @propBP.route('/seller_properties')
    def seller_view_properties():
        properties = sellerPropertiesController.seller_viewProperties()
        return render_template('property/seller_properties.html', properties=properties)
