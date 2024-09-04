from flask import Flask
from routes import bp as routes_bp

# Setting up Flask
app = Flask(__name__)

# Setting up Blueprint to modularize
# the routes
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    # Running the app. user_reloader has to be true
    # to make OpenCV work with Flask
    app.run(debug=True, host='0.0.0.0', use_reloader=False) 