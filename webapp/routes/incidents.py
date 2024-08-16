import os
from flask import render_template
from . import bp

@bp.route('/incidents')
def incidents():
    thumbnails_folder = os.path.join(os.path.dirname(__file__), '..', 'static', 'thumbnails')
    thumbnails = [f for f in os.listdir(thumbnails_folder) if f.endswith('.jpg')]
    return render_template('incidents.html', thumbnails=thumbnails)
