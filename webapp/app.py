from flask import Flask
from routes import bp as routes_bp

app = Flask(__name__)

app.register_blueprint(routes_bp)


# app.register_blueprint(routes_bp)

if __name__ == '__main__':
    # use_reloader is needed to be False otherwise OpenCV 
    # does not with Flask work in RPi
    app.run(debug=True, host='0.0.0.0', use_reloader=False) 