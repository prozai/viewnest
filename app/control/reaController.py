from flask import render_template, redirect, url_for, request
from flask_babel import _
from app.entity.models import Review, User
from app import Session

class reaReviewController:
    def view_reviews(self, rea_id):
        reviews = Review.get_reviews_by_rea_id(rea_id)
        return reviews
