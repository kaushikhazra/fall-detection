from flask import Blueprint

# Create a blueprint
bp = Blueprint('routes', __name__)

# Import all routes to register them with the blueprint
from . import home, live_feed, incidents
