from VideoCapture import VideoCapture
from MovementDetector import MovementDetector
from FallDetector import FallDetector
from VideoRecorder import VideoRecorder
from EmailSender import EmailSender

class DetectionPipeline():
    '''
    The detection pipeline class. This class is
    responsible for running detection workflow
    '''

    def __init__(self):
        '''
        Constructor setting up video capture, movement
        detection, fall detection, video recorder and
        email sender.

        Video recorder is configured to record a 10 second
        video after the fall is detected

        Email sender is configured to send email to the same
        account.
        '''
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
        '''
        The method that starts the workflow
        '''
        try:
            while True:
                self.capture_video()
        except KeyboardInterrupt:
            self.video_capture.release()
            


    def capture_video(self):
        '''
        This step captures the video frame and
        saves it to a class variable. If video
        capture of an existing fall is in progress
        then the recorder step is call, otherwise 
        the movement detection step is called
        '''
        self.frame = self.video_capture.capture_frame()
        if not self.recording_video:
            self.detect_movement()
        else :
            self.record_video()

    
    def detect_movement(self):
        '''
        Detects movement. If movement is detected
        forwards the control to fall detector
        '''
        if self.movement_detector.detect_movement(self.frame):
             print("Movement Detected")
             self.detect_fall()
    

    def detect_fall(self):
        '''
        Detects fall. If fall is detected the control
        is transferred to video recording
        '''
        if self.fall_detector.detect_fall(self.frame):
            print("Fall Detected")
            self.record_video()
    
    def record_video(self):
        '''
        This step records the video. It opens a stream
        to the video file and channels the frames captured
        in the capture_video step to the file, until the
        desired duration is not met. Default is 10 sec of
        recording
        '''
        if not self.recording_video:
            self.video_recorder.initialize(self.frame)
            self.recording_video = True

        if not self.video_recorder.record_frame(self.frame):
            self.recording_video = False
            self.video_recorder.finalize()
            self.send_email()


       
    def send_email(self):
        '''
        This step sends email to the configured user after
        a fall is detect
        '''
        self.email_sender.send_email(self.video_recorder.thumbnail_path) 

