import cv2

class VideoCapture:
    '''
    Class that captures a frame using 
    OpenCV
    '''
    def __init__(self, video_file):
        self.video_input = None
        self.video_file = video_file       

    def capture_frame(self):
        '''
        This method captures a frame from the
        camera using OpenCV Video Capture
        '''
        if self.video_input is None:
            if self.video_file is not None:
                print('Reading from file ' + self.video_file)
                self.video_input = cv2.VideoCapture(self.video_file)
            else:
                # The 0 represents the camera
                self.video_input = cv2.VideoCapture(0)

        if not self.video_input.isOpened() and self.video_file is None:
            print('Error: Could not open camera.')
            return None
        else:
            # Reads the frame from video device
            ret, frame = self.video_input.read()
            if not ret:
                print('Error: Could not read frame.')
                return None
            return frame

    def release(self):
        '''
        Releases the camera stream
        '''
        if self.video_input is not None:
            self.video_input.release()
            self.video_input = None