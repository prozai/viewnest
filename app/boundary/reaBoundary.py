from flask import render_template, request, redirect
from app.control.reaController import *
from app.control.loginController import loginController
from app.boundary import reaBP

class reaBoundary:
    def view_reviews(self):
        if request.method == 'GET':
            #pass user id thru
            result = loginController.dashboard()
            if 'redirect' in result:
                return redirect(result['redirect'])
            user = result.get('user')

            print("Real Estate Agent ID: "+ str(user.user_id))
            # retrieve all reviews for the real estate agent with the given ID
            reaController = reaReviewController()
            reviews = reaController.view_reviews(user.user_id)
            print(reviews)
            #return redirect('/viewReviews')
        return render_template('REAgent/view-reviews.html', reviews=reviews)
    
reaBoundary = reaBoundary()
@reaBP.route('/viewReviews', methods=['GET', 'POST'])
def view_review():    
    return reaBoundary.view_reviews()