from flask import render_template, redirect, url_for, request
from flask_babel import _
from app.entity.models import Review, User
from app import Session

# Create Buyer Controller
class ReviewController:
    def addReview(self, rating, review, user_id, rea_email):
        rea_email_status = User.check_email(rea_email)
        print(rea_email_status)
        if not rea_email_status:
            return _("Please enter a valid email.")
        else:
            rea_id = User.retrieve_rea_id_by_email(rea_email)
            print(rea_id)
            review = Review(rating, review, user_id, rea_id)
            status = Review.create_new_review(review=review)
            return status