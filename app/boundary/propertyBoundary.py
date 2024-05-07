from flask import render_template
from app.control.propertyController import add_sample_properties, show_all_properties, get_property, add_viewCount
from app.control import bp

@bp.route('/view_properties')
def view_properties():
    add_sample_properties()
    properties = show_all_properties()
    return render_template('property/view_properties.html', properties=properties)

@bp.route('/view_calculation')
def view_calculation():
    return render_template('property/view_calculation.html')

@bp.route('/view_property_detail/<int:property_id>')
def view_property_detail(property_id):
    property = get_property(property_id)
    add_viewCount(property_id)
    return render_template('property/view_property_detail.html', property=property)