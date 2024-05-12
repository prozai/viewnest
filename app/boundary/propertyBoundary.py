from flask import render_template, redirect, url_for
from app.control.propertyController import *
from app.control import bp

class createPropertyBoundary:
    def createProperty(self):
        createPropertyController.REA_createProperty()
        return render_template('REAgent/create_property.html')
    
class REAPropertiesBoundary:
    def REAViewProperties(self):
        properties = REAPropertiesController.REA_viewProperties()
        return render_template('REAgent/REA_properties.html', properties=properties)

class updatePropertyBoundary:
    def updateProperty(self, id):
        property = updatePropertyController.REA_updateProperty(id)
        return render_template('REAgent/update_property.html', property=property)
    
class deletePropertyBoundary:
    def deleteProperty(self, id):
        deletePropertyController.REA_deleteProperty(id)
        return redirect(url_for('route.REA_view_properties'))

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

class savePropertyBoundary:
    def saveProperty(self):
        savePropertyController.buyer_saveProperty()
        return redirect(url_for('route.view_properties'))

class sellerPropertiesBoundary:
    def sellerViewProperties(self):
        properties = sellerPropertiesController.seller_viewProperties()
        return render_template('property/seller_properties.html', properties=properties)
    
create_property_boundary = createPropertyBoundary()
REA_properties_boundary = REAPropertiesBoundary()
update_property_boundary = updatePropertyBoundary()
delete_property_boundary = deletePropertyBoundary()
property_boundary = viewPropertyBoundary()
save_property_boundary = savePropertyBoundary()
seller_properties_boundary = sellerPropertiesBoundary()

@bp.route('/create_property', methods=['GET', 'POST'])
def create_property():
    return create_property_boundary.createProperty()

@bp.route('/REA_properties')
def REA_view_properties():
    return REA_properties_boundary.REAViewProperties()

@bp.route('/update_property/<int:id>/', methods=['GET', 'POST'])
def update_property(id):
    return update_property_boundary.updateProperty(id)

@bp.route('/delete_property/<int:id>/', methods=['POST'])
def delete_property(id):
    return delete_property_boundary.deleteProperty(id)

@bp.route('/view_properties')
def view_properties():
    return property_boundary.view_properties()
    
@bp.route('/view_calculation')
def view_calculation():
    return property_boundary.view_calculation()

@bp.route('/view_property_detail/<int:property_id>')
def view_property_detail(property_id):
    return property_boundary.view_property_detail(property_id)

@bp.route('/save_property', methods=['POST'])
def save_property():
    return save_property_boundary.saveProperty()

@bp.route('/seller_properties')
def seller_view_properties():
    return seller_properties_boundary.sellerViewProperties()