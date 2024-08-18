from prefect import Flow, task

from VideoCapture import VideoCapture
from MovementDetector import MovementDetector
from FallDetector import FallDetector
from VideoRecorder import VideoRecorder
from EmailSender import EmailSender

class DetectionPipeline():

    def __init__(self):
        self.video_capture = VideoCapture()
        self.movement_detector = MovementDetector()
        self.fall_detector = FallDetector()
        self.video_recorder = VideoRecorder(recording_duration=10)
        self.email_sender = EmailSender(
            smtp_server = 'smtp.office365.com',
            smtp_port = 587,
            sender_email = 'kaushik.hazra.uol@outlook.com',
            sender_password = 'k@ush1kh@zr@',
            recipient_email = 'kaushik.hazra.uol@outlook.com'
        )

        self.recording_video = False


    def start(self):
        try:
            while True:
                self.capture_video()
        except KeyboardInterrupt:
            self.video_capture.release()
            


    def capture_video(self):
        self.frame = self.video_capture.capture_frame()
        if not self.recording_video:
            self.detect_movement()
        else :
            self.record_video()

    
    def detect_movement(self):
        if self.movement_detector.detect_movement(self.frame):
             print("Movement Detected")
             self.detect_fall()
    
    def detect_fall(self):
        if self.fall_detector.detect_fall(self.frame):
            print("Fall Detected")
            self.record_video()
    
    def record_video(self):
        if not self.recording_video:
            self.video_recorder.initialize(self.frame)
            self.recording_video = True

        if not self.video_recorder.record_frame(self.frame):
            self.recording_video = False
            self.video_recorder.finalize()
            self.send_email()


       
    def send_email(self):
        self.email_sender.send_email(self.video_recorder.thumbnail_path) 

