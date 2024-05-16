from flask import render_template, request, redirect
from app.control.reviewController import *
from app.control.loginController import loginController
from app.boundary import buyerBP

class buyerBoundary:
    def addReview(self):
        if request.method == 'POST':
            #pass user id thru
            result = loginController.dashboard()
            if 'redirect' in result:
                return redirect(result['redirect'])
            user = result.get('user')

            print(user.user_id)  
            review = request.form.get('review')
            rating = request.form.get('rating')
            rea_email = request.form.get('rea-email')
            print(rea_email)

            #check if rea-email is valid
            

            user_id = user.user_id

            add_review = ReviewController()
            review_status = add_review.addReview(review, rating, user_id, rea_email)
            print(review_status)
            return redirect('/addReview')
        return render_template('buyer/create-review.html')
    
buyerBoundary = buyerBoundary()
@buyerBP.route('/addReview', methods=['GET', 'POST'])
def create_review():    
    return buyerBoundary.addReview()