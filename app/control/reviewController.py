from flask import render_template, redirect, url_for, request
from flask_babel import _
from app.entity.models import Review, User
from app import Session

# Create Buyer Controller
class ReviewController:
    def addReview(self, review, rating, user_id, rea_email):
        try:
            rea_id = User.retrieve_rea_id_by_email(rea_email)
            if rea_id is None:
                status = False
                print("add review:"+ status)
                return status
            else:
                print("REA ID: " + str(rea_id))
                review = Review(review, rating, user_id, rea_id)
                status = Review.create_new_review(review=review)
                print("add review:"+ status)
                return status
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred while adding review: {str(e)}")
            status = "nu good"
            return status
        
    def checkEmail(self, email):
        status = User.check_email(email)
        # print("checkEmail :" + str(status))
        if status is True:
            status = True
        else:
            status = False
        return status