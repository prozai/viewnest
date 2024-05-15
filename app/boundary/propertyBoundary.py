from flask import render_template, request, redirect, url_for
from app.control.propertyController import *
from app.control.loginController import loginController
from app.boundary import propBP

class viewPropertyBoundary:
    @propBP.route('/view_properties')
    def view_properties():
        #Get user for HTML page
        result = loginController.dashboard()       
        user = result.get('user')                
     #  viewPropertyController.add_sample_properties()
        properties = viewPropertyController.view_properties()
        return render_template('property/view_properties.html', user=user , properties=properties )

    @propBP.route('/view_calculation')
    @loginController.login_required
    def view_calculation():
        #Get user for HTML page
        result = loginController.dashboard()       
        user = result.get('user')           
        return render_template('property/view_calculation.html', user=user)

    @propBP.route('/view_property_detail/<int:property_id>')
    @loginController.login_required
    def view_property_detail(property_id):
        #Get user for HTML page
        result = loginController.dashboard()       
        user = result.get('user')        
                
        property = viewPropertyController.view_property_detail(property_id)
        viewCountController.add_viewCount(property_id)
        return render_template('property/view_property_detail.html', property=property, user=user)
    
property_boundary = viewPropertyBoundary()


class createPropertyPage():
    @propBP.route('/create_property', methods=['GET', 'POST'])
    def create_property():

        #Get user for HTML page
        result = loginController.dashboard()       
        user = result.get('user')

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
        return render_template('REAgent/create_property.html',user=user)
    
class REAPropertiesPage:
    @propBP.route('/REA_properties')
    def REA_view_properties():
        #Get user for HTML page
        result = loginController.dashboard()       
        user = result.get('user')        
        properties = REAPropertiesController.REA_viewProperties()
        return render_template('REAgent/REA_properties.html', properties=properties,user = user)
    
class updatePropertyPage:
    @propBP.route('/update_property/<int:id>/', methods=['GET', 'POST'])
    def update_property(id):
        #Get user for HTML page
        result = loginController.dashboard()       
        user = result.get('user')        
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
        return render_template('REAgent/update_property.html', property=property,user = user)
    
class deleteProperty:
    @propBP.route('/delete_property/<int:id>/', methods=['POST'])
    def delete_property(id):
        #Get user for HTML page
        result = loginController.dashboard()       
        user = result.get('user')        
        try:
            deletePropertyController.REA_deleteProperty(id)
        except Exception as e:
            flash("Error deleting property: " + str(e))
        
        flash("Deleted successfully!")
        return redirect(url_for('propRoutes.REA_view_properties'))

class saveProperty:
    @propBP.route('/save_property', methods=['POST'])
    
    def save_property():
        #Get user for HTML page
        result = loginController.dashboard()       
        user = result.get('user')
        savePropertyController.buyer_saveProperty()
        return redirect(url_for('propRoutes.view_properties'))

class sellerPropertiesPage:
    @propBP.route('/seller_properties')
    def seller_view_properties():
        #Get user for HTML page
        result = loginController.dashboard()       
        user = result.get('user')
                
        properties = sellerPropertiesController.seller_viewProperties()
        return render_template('property/seller_properties.html', properties=properties, user = user)
#search

class SearchPropertyBoundary:
    def __init__(self):
        self.controller = SearchController()
        
    def search(self, search_query):
        results = self.controller.search(search_query)
        return render_template('property/search.html', results=results)

    def searchSold(self, search_query):
        results = self.controller.searchSold(search_query)
        return render_template('property/search.html', results=results)

    def searchAvailable(self, search_query):
        results = self.controller.searchAvailable(search_query)
        return render_template('property/search.html', results=results)

search_boundary = SearchPropertyBoundary()


@propBP.route('/search', methods=['POST', 'GET'])
@loginController.login_required
def search():
    search_query = request.form.get('query')
    return search_boundary.search(search_query)


@propBP.route('/searchSold', methods=['POST', 'GET'])
@loginController.login_required
def searchSold():
    search_query = request.form.get('query')
    return search_boundary.searchSold(search_query)

@propBP.route('/searchAvailable', methods=['POST', 'GET'])
@loginController.login_required
def searchAvailable():
    search_query = request.form.get('query')
    return search_boundary.searchAvailable(search_query)