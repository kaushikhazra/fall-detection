import cv2

class MovementDetector:
    '''
    The movement detection class
    '''
    def __init__(self):
        # Setting up the Mixture of Gaussian background subtractor
        self.background_subtractor = cv2.createBackgroundSubtractorMOG2()

    def detect_movement(self, frame):
        '''
        Method that detects movements
        '''
        # Creating the foreground mask
        foreground_mask = self.background_subtractor.apply(frame)
        
        # Find the contour data for foreground
        contour_data = cv2.findContours(foreground_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        # I have found out that in OpenCV 3.2 this method returns 3 parameters, however
        # in OpenCV 4.8 it returns 2 parameters. Because I used the same code for my PC
        # and my Raspberry Pi (which is little older) I had to create this work around
        # to get the contour
        if len(contour_data) == 3:
            contours = contour_data[1]
        else:
            contours = contour_data[0]

        # Count the contours which are bigger than 
        # 1000
        contour_count = 0
        for contour in contours:
            if cv2.contourArea(contour) > 1000:
                contour_count += 1

        # If we find a contour then return
        # true or return false
        return contour_count > 0