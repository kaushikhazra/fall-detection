from flask import render_template
from . import bp

# Exposing the route for the Home
@bp.route('/')
def home():
    return render_template('home.html')

# Exposing the route for the About Page
@bp.route('/about')
def about():
    return render_template('about.html')
