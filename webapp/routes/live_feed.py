from flask import Response, jsonify
import cv2
from . import bp

# camera = cv2.VideoCapture(0)  # Use 0 for web camera
camera = None
continue_frame_generation = True

def generate_frames():
    global camera
    while continue_frame_generation:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    camera.release()
    camera = None

@bp.route('/live_feed')
def live_feed():
    print('Starting camera')
    global continue_frame_generation, camera
    camera = cv2.VideoCapture(0) 
    continue_frame_generation = True
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/stop_camera')
def stop_camera():
    print('Stopping camera')
    global continue_frame_generation
    continue_frame_generation = False
    return jsonify({"status": "camera stopped"})
