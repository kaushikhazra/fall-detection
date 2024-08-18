import cv2
import torch
import smtplib
from datetime import datetime
from nanodet_predictor import Predictor
from person_detector import PersonDetector
from nanodet.util import cfg, load_config, Logger
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders

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
        thumbnail_path = f"../webapp/static/thumbnails/{creation_date}.jpg"
        cv2.imwrite(thumbnail_path, thumbnail)  # Save the thumbnail
        video_writer = cv2.VideoWriter(f"../webapp/static/videos/{creation_date}.mp4", fourcc, 20.0, (640, 480))
        send_email(thumbnail_path)
    
    current_date_time = f"{current_date}-{current_hour}-{current_minute}"

    if creation_date != current_date_time:
        video_writer.release()
        creation_date = current_date_time
        thumbnail = cv2.resize(frame, thumbnail_size, interpolation=cv2.INTER_AREA)
        thumbnail_path = f"../webapp/static/thumbnails/{creation_date}.jpg"
        cv2.imwrite(thumbnail_path, thumbnail)  # Save the thumbnail
        video_writer = cv2.VideoWriter(f"../webapp/static/videos/{creation_date}.mp4", fourcc, 20.0, (640, 480))
        send_email(thumbnail_path)

    video_writer.write(frame)


#----------- Record Video --------------------------#

#----------- Send Email --------------------------#
smtp_server = 'smtp.office365.com'
smtp_port = 587
sender_email = 'kaushik.hazra.uol@outlook.com'
sender_password = 'k@ush1kh@zr@'

def send_email(image_path):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = 'kaushik.hazra.uol@outlook.com'
    msg['Subject'] = '!!URGENT!FALL AT CAM1 LOCATION !!'

    image_cid = 'image1'
    html_body = f"""
    <html>
    <body>
        <p>Dear User,</p>
        <p>Incident detected at CAM1 that needs your ATTENTION!</p>
        <img src="cid:{image_cid}" alt="Clickable Image" style="width:300px;height:auto;">
        <p>
        <a href="https://www.example.com">
            Click here to see the video
        </a>
        </p>
        <p>
        Thank you,<br/>
        Fall Detection System
        </p>
    </body>
    </html>
    """

    msg.attach(MIMEText(html_body, 'html'))

    with open(image_path, 'rb') as img_file:
        img = MIMEImage(img_file.read(), name='image.jpg')
        img.add_header('Content-ID', f'<{image_cid}>')
        msg.attach(img)

    try:
        print('Sending Email')
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls() 
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, msg['To'], text)
        
        print('Email sent successfully!')
    except Exception as e:
        print(f'Failed to send email: {e}')
    finally:
        pass
        # server.quit()

#----------- Send Email --------------------------#

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
            # If fall is detected 
            if fall_detected:
                print("Fall detected")
                record_video(frame)

            else:
                pass
                # print("No fall detected")
            # If NO fall detected 

                # Continue

        # If no movement detected continue
        else :
            pass
            # print("No Movement")
            

except KeyboardInterrupt:
    video_input.release()
    video_writer.release()
    cv2.destroyAllWindows()