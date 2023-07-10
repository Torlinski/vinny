from flask import Blueprint, render_template

index = Blueprint('index', __name__)

@index.route('/')
def home():
    """Return index page"""
    return render_template('index.html') # this is the index.html file in the templates folder