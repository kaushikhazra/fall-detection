import cv2
from datetime import datetime, timedelta

class VideoRecorder:
    '''
    This class takes a frame and
    saves it in a file. It does that till
    the duration specified in recording_duration.

    This class does not block the ongoing pipeline
    it signals the pipeline when the duration is up
    and the pipeline can stop directing the frames to
    the video recorder
    '''
    def __init__(self, recording_duration=30, video_resolution=(640, 480), thumbnail_size=(150, 150)):
        self.fourcc = cv2.VideoWriter_fourcc(*'avc1')
        self.recording_duration = recording_duration
        self.video_resolution = video_resolution
        self.thumbnail_size = thumbnail_size
        self.video_writer = None
        self.start_time = None
        self.thumbnail_path = None
        self.video_path = None

    def initialize(self, frame):
        now = datetime.now()
        creation_date = f"{now.date()}-{now.hour}-{now.minute}"
        self.thumbnail_path = f"../webapp/static/thumbnails/{creation_date}.jpg"
        self.video_path = f"../webapp/static/videos/{creation_date}.mp4"
        
        thumbnail = cv2.resize(frame, self.thumbnail_size, interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.thumbnail_path, thumbnail)
        self.video_writer = cv2.VideoWriter(self.video_path, self.fourcc, 20.0, self.video_resolution)
        self.start_time = now

    def record_frame(self, frame):
        if self.video_writer is None:
            self.initialize(frame)
        
        self.video_writer.write(frame)
        
        if (datetime.now() - self.start_time).seconds >= self.recording_duration:
            return False
        
        return True

    def finalize(self):
        if self.video_writer is not None:
            self.video_writer.release()
            self.video_writer = None
        print(f"Video recording completed. Duration: {self.recording_duration} seconds")
        print(f"Video saved to: {self.video_path}")
        print(f"Thumbnail saved to: {self.thumbnail_path}")
        return self.thumbnail_path