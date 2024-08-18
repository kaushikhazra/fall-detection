import cv2

class VideoCapture:
    def __init__(self):
        self.video_input = None

    def capture_frame(self):
        if self.video_input is None:
            self.video_input = cv2.VideoCapture(0)

        if not self.video_input.isOpened():
            print('Error: Could not open camera.')
            return None
        else:
            ret, frame = self.video_input.read()
            if not ret:
                print('Error: Could not read frame.')
                return None
            return frame

    def release(self):
        if self.video_input is not None:
            self.video_input.release()
            self.video_input = None