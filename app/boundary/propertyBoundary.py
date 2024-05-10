from flask import render_template, redirect, url_for
from app.control.propertyController import createPropertyController, viewPropertiesController, updatePropertyController, deletePropertyController
from app.control import bp

class createPropertyBoundary:
    def __init__(self):
        self.controller = createPropertyController()
        
    def createProperty(self):
        self.controller.REA_createProperty()
        return render_template('REAgent/create_property.html')
    
class REAPropertiesBoundary:
    def __init__(self):
        self.controller = viewPropertiesController()
        
    def REAViewProperties(self):
        properties = self.controller.REA_viewProperties()
        return render_template('REAgent/REA_properties.html', properties=properties)

class updatePropertyBoundary:
    def __init__(self):
        self.controller = updatePropertyController()
        
    def updateProperty(self, id):
        property = self.controller.REA_updateProperty(id)
        return render_template('REAgent/update_property.html', property=property)
    
class deletePropertyBoundary:
    def __init__(self):
        self.controller = deletePropertyController()
        
    def deleteProperty(self, id):
        self.controller.REA_deleteProperty(id)
        return redirect(url_for('route.REA_view_properties'))
    
create_property_boundary = createPropertyBoundary()
REA_properties_boundary = REAPropertiesBoundary()
update_property_boundary = updatePropertyBoundary()
delete_property_boundary = deletePropertyBoundary()

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
