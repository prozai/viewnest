
from flask import render_template, redirect, url_for, request
from flask_babel import _
from app.entity.models import Review
from app import Session

from app.control import buyerBP

# Create Buyer Controller
class addReviewController():
    @buyerBP.route('/addReview', methods=['GET', 'POST'])
    def addReview():
        if request.method == "POST":
            try:
                review = request.form.get("review")
                rating = request.form.get("rating")
                user_id = request.form.get("user_id")
                review = Review(review, rating, user_id)
                Review.create_new_review(review)
                print(review)

            except Exception as e:
                print(e)
        return render_template('buyer/create-review.html')
