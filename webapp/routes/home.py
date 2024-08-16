from flask import render_template
from . import bp

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/about')
def about():
    return render_template('about.html')

@bp.route('/go_live')
def go_live():
    return render_template('go_live.html')
