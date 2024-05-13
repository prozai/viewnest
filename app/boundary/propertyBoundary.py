from flask import render_template, request, redirect, url_for
from app.control.propertyController import *
from app.control.loginController import loginController
from app.boundary import propBP

class viewPropertyBoundary:
    def view_properties(self):
     #  viewPropertyController.add_sample_properties()
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



class createPropertyBoundary:
    def __init__(self):
        self.controller = createPropertyController()
        
    def createProperty(self):
        #pass user id thru
        result = loginController.dashboard()
        if 'redirect' in result:
            return redirect(result['redirect'])
        user = result.get('user')        
        #pass user id thru

        self.controller.REA_createProperty()
        return render_template('REAgent/create_property.html',user=user)
    
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
        return redirect(url_for('propRoutes.REA_view_properties'))

class savePropertyBoundary:
    def saveProperty(self):
        savePropertyController.buyer_saveProperty()
        return redirect(url_for('propRoutes.view_properties'))

class sellerPropertiesBoundary:
    def sellerViewProperties(self):
        properties = sellerPropertiesController.seller_viewProperties()
        return render_template('property/seller_properties.html', properties=properties)
    


create_property_boundary = createPropertyBoundary()
REA_properties_boundary = REAPropertiesBoundary()
update_property_boundary = updatePropertyBoundary()
delete_property_boundary = deletePropertyBoundary()
save_property_boundary = savePropertyBoundary()
seller_properties_boundary = sellerPropertiesBoundary()

@propBP.route('/create_property', methods=['GET', 'POST'])
def create_property():
    return create_property_boundary.createProperty()

@propBP.route('/REA_properties')
def REA_view_properties():
    return REA_properties_boundary.REAViewProperties()

@propBP.route('/update_property/<int:id>/', methods=['GET', 'POST'])
def update_property(id):
    return update_property_boundary.updateProperty(id)

# Delete Property Listing
@propBP.route('/delete_property/<int:id>/', methods=['POST'])
def delete_property(id):
    return delete_property_boundary.deleteProperty(id)

@propBP.route('/save_property', methods=['POST'])
def save_property():
    return save_property_boundary.saveProperty()

@propBP.route('/seller_properties')
def seller_view_properties():
    return seller_properties_boundary.sellerViewProperties()