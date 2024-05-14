from flask import render_template, redirect, url_for, request
from flask_babel import _
from app.entity.models import Review
from app import Session

# Create Buyer Controller
class addReviewController():
    
    def add_review(review, rating, user_id):
        review = request.form.get("review")
        rating = request.form.get("rating")
        # user_id = request.form.get("user_id")
        user_id = 2
        review = Review(review, rating, user_id)
        Review.create_new_review(review)
        print(review)
        return {'redirect': '/addReviews'}
    def view_reviews():
        reviews = Session.query(Review).all()
        return reviews
