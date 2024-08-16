import os
import cv2

# Path to the videos folder
videos_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static', 'videos'))
# Path to the thumbnails folder
thumbnails_folder = os.path.join(os.path.dirname(__file__), 'static', 'thumbnails')

# Create the thumbnails folder if it doesn't exist
if not os.path.exists(thumbnails_folder):
    os.makedirs(thumbnails_folder)

# Iterate through each video in the videos folder
for video_file in os.listdir(videos_folder):
    if video_file.endswith(('.mp4', '.avi', '.mov')):
        video_path = os.path.join(videos_folder, video_file)
        thumbnail_path = os.path.join(thumbnails_folder, f"{os.path.splitext(video_file)[0]}.jpg")

        # Capture the video
        cap = cv2.VideoCapture(video_path)
        ret, frame = cap.read()
        if ret:
            # Save the first frame as the thumbnail
            cv2.imwrite(thumbnail_path, frame)
        cap.release()
