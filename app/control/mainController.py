from flask import render_template, flash, redirect, url_for
from flask_babel import _
from app.control import mainBP

@mainBP.route('/')
def index():
    return render_template('index.html', title="")

@mainBP.route('/adminIndex')
def adminIndex():
    return render_template('systemAdmin/index.html', title="")
