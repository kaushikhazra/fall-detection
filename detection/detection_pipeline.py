import cv2
import torch
from datetime import datetime
from nanodet_predictor import Predictor
from person_detector import PersonDetector
from nanodet.util import cfg, load_config, Logger

#----------- Capture Frame --------------------------#
video_input = None
def capture_frame():
    global video_input
    if video_input is None:
        video_input = cv2.VideoCapture(0)

    if not video_input.isOpened():
        print('Error: Could not open camera.')
        return None
    else :
        ret, frame = video_input.read()
        return frame
#----------- Capture Frame --------------------------#

#----------- Movement detection --------------------------#
background_subtractor = cv2.createBackgroundSubtractorMOG2()
def detect_movement(frame):
    foreground_mask = background_subtractor.apply(frame)
    contours = None
    contour_data = cv2.findContours(foreground_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # I have found out that in OpenCV 3.2 this method returns 3 parameters, however
    # in OpenCV 4.8 it returns 2 parameters. Because I used the same code for my PC
    # and my Raspberry Pi (which is little older) I had to create this work around
    # to get the contour
    if len(contour_data) == 3:
        contours = contour_data[1]
    else :
        contours = contour_data[0]

    contour_count = 0
    for contour in contours:
        if cv2.contourArea(contour) > 1000 :
            contour_count += 1

    # print(contour_count)
    return contour_count > 0

#----------- Movement detection --------------------------#

#----------- Fall detection --------------------------#
predictor = None
detector = None
def detect_fall(frame):
    global predictor
    global detector
    if predictor is None:
        config_path = 'nanodet_m.yml'
        model_path = 'nanodet_m.ckpt'
        load_config(cfg, config_path)
        logger = Logger(-1, use_tensorboard=False)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        predictor = Predictor(cfg, model_path, logger, device=device)

    if detector is None:
        detector = PersonDetector()

    
    score_thres = 0.35
    meta, res = predictor.inference(frame)
    fall_detected = detector.detect(res, score_thres)

    return fall_detected
#----------- Fall detection --------------------------#

#----------- Record Video --------------------------#
video_writer = None
creation_date = None
fourcc = cv2.VideoWriter_fourcc(*'avc1')
thumbnail_size = (150, 150)
def record_video(frame):
    global video_writer
    global creation_date
    
    now = datetime.now()
    current_date = now.date()
    current_hour = now.hour
    current_minute = now.minute

    if video_writer is None:
        creation_date = f"{current_date}-{current_hour}-{current_minute}"
        thumbnail = cv2.resize(frame, thumbnail_size, interpolation=cv2.INTER_AREA)
        cv2.imwrite(f"../webapp/static/thumbnails/{creation_date}.jpg", thumbnail)  # Save the thumbnail
        video_writer = cv2.VideoWriter(f"../webapp/static/videos/{creation_date}.mp4", fourcc, 20.0, (640, 480))
    
    current_date_time = f"{current_date}-{current_hour}-{current_minute}"

    if creation_date != current_date_time:
        video_writer.release()
        creation_date = current_date_time
        thumbnail = cv2.resize(frame, thumbnail_size, interpolation=cv2.INTER_AREA)
        cv2.imwrite(f"../webapp/static/thumbnails/{creation_date}.jpg", thumbnail)  # Save the thumbnail
        video_writer = cv2.VideoWriter(f"../webapp/static/videos/{creation_date}.mp4", fourcc, 20.0, (640, 480))

    video_writer.write(frame)


#----------- Record Video --------------------------#

try:
    while True:
        # Receive Video Frame
        frame = capture_frame()

        # Detect any movement using FD & BS
        movement_detected = detect_movement(frame)

        # If movement is detected
        if movement_detected:
            print("Movement")
            # Use NenoDet NN to detect fall
            fall_detected = detect_fall(frame)
            record_video(frame)
            # If fall is detected 
            if fall_detected:
                print("Fall detected")
                record_video(frame)
                # record a 10 sec. video and save it in the file
                # record_video(frame)

            else:
                print("No fall detected")
            # If NO fall detected 

                # Continue

        # If no movement detected continue
        else :
            print("No Movement")

except KeyboardInterrupt:
    video_input.release()
    video_writer.release()
    cv2.destroyAllWindows()