from flask import render_template, request, redirect
from app.control.reviewController import *
from app.control.loginController import loginController
from app.boundary import sellerBP

class sellerBoundary:
    def addReview(self):
        if request.method == 'POST':
            try:
                #pass user id thru
                result = loginController.dashboard()
                if 'redirect' in result:
                    return redirect(result['redirect'])
                user = result.get('user')

                print("current user ID" + str(user.user_id))
                review = request.form.get('review')
                rating = request.form.get('rating')
                rea_email = request.form.get('rea-email')
                print(rea_email)
                reviewController = ReviewController()
                #check if rea-email is valid
                user_id = user.user_id
                review_status = reviewController.checkEmail(rea_email)
                # print("Review status:"+str(review_status))
                if (review_status is False):
                    return render_template('seller/create-review.html', error="Email does not exist")
                if(review_status is True):
                    add_review_status = reviewController.addReview(review, rating, user_id, rea_email)
                    if add_review_status is False:
                        return render_template('seller/create-review.html', error="Error adding review")
                    message = "Review added successfully!"
                    print(message)
                return render_template('seller/create-review.html', message=message)
            except Exception as e:
                # handle the exception here
                print(f"An error occurred: {str(e)}")
                # return an error message or redirect to an error page
        return render_template('seller/create-review.html')

sellerBoundary = sellerBoundary()
@sellerBP.route('/sellerAddReview', methods=['GET', 'POST'])
def create_review():    
    return sellerBoundary.addReview()