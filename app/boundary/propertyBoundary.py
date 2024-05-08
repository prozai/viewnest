from flask import render_template, redirect, url_for
from app.control.propertyController import createPropertyController, viewPropertiesController, updatePropertyController, deletePropertyController
from app.control import bp

@bp.route('/create_property', methods=['GET', 'POST'])
def create_property():
    createPropertyController.REA_createProperty()
    return render_template('REAgent/create_property.html')

@bp.route('/REA_properties')
def view_REA_properties():
    properties = viewPropertiesController.REA_viewProperties()
    return render_template('REAgent/REA_properties.html', properties=properties)

@bp.route('/update_property/<int:id>/', methods=['GET', 'POST'])
def update_property(id):
    property = updatePropertyController.REA_updateProperty(id)
    return render_template('REAgent/update_property.html', property=property)

# Delete Property Listing
@bp.route('/delete_property/<int:id>/', methods=['POST'])
def delete_property(id):
    deletePropertyController.REA_deleteProperty(id)
    return redirect(url_for('route.view_REA_properties'))