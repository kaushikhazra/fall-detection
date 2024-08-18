import cv2

class MovementDetector:
    def __init__(self):
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()

    def detect_movement(self, frame):
        # Apply the background subtractor to get the foreground mask
        foreground_mask = self.background_subtractor.apply(frame)
        
        # Find contours in the foreground mask
        contour_data = cv2.findContours(foreground_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # Handle the difference between OpenCV versions in the number of returned values
        if len(contour_data) == 3:
            contours = contour_data[1]
        else:
            contours = contour_data[0]

        # Count the number of significant contours
        contour_count = 0
        for contour in contours:
            if cv2.contourArea(contour) > 1000:  # Filter out small contours
                contour_count += 1

        # Return True if movement is detected (i.e., there are significant contours)
        return contour_count > 0