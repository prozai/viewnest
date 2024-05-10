from flask import render_template, request
from app.control.propertyController import viewCountController, viewPropertyController
from app.boundary import propBP

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

@propBP.route('/view_properties')
def view_properties():
    return property_boundary.view_properties()
    
@propBP.route('/view_calculation')
def view_calculation():
    return property_boundary.view_calculation()

@propBP.route('/view_property_detail/<int:property_id>')
def view_property_detail(property_id):
    return property_boundary.view_property_detail(property_id)