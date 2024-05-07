from flask import render_template, request
from app.control.propertyController import SearchController
from app.control import bp

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


@bp.route('/search', methods=['POST', 'GET'])
def search():
    search_query = request.form.get('query')
    return search_boundary.search(search_query)


@bp.route('/searchSold', methods=['POST', 'GET'])
def searchSold():
    search_query = request.form.get('query')
    return search_boundary.searchSold(search_query)

@bp.route('/searchAvailable', methods=['POST', 'GET'])
def searchAvailable():
    search_query = request.form.get('query')
    return search_boundary.searchAvailable(search_query)