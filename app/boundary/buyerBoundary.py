from flask import render_template, request, redirect
from app.control.buyerController import *
from app.boundary import buyerBP

class buyerBoundary:
    def addReview(self):
        if request.method == 'POST':
            review = request.form.get('review')
            rating = request.form.get('rating')
            user_id = request.form.get('user_id')
            review = Review(review, rating, user_id)
            add_review = ReviewController.addReview(review)
            print(add_review)
            # success = add_review.add_review(review, rating, user_id)
            return redirect('/addReview')
        return render_template('buyer/create-review.html')
    
    # def view_reviews(self):
    #     reviews = buyerController.view_reviews()
    #     return render_template('buyer/view-reviews.html', reviews=reviews)

buyerBoundary = buyerBoundary()
@buyerBP.route('/addReview', methods=['GET', 'POST'])
def create_review():    
    return buyerBoundary.addReview()