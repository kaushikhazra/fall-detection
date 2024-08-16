from flask import Response
import cv2
from . import bp

camera = cv2.VideoCapture(0)  # Use 0 for web camera

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@bp.route('/live_feed')
def live_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
