from flask import render_template, redirect, url_for, request
from flask_babel import _
from app.entity.models import Review
from app import Session

# Create Buyer Controller
class ReviewController:
    def addReview(self, rating, review, user_id):
        review = Review(rating, review, user_id)
        status = Review.create_new_review(review=review)
        return status
    
    def view_reviews(self):
        reviews = Session.query(Review).all()
        return reviews
