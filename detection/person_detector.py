class PersonDetector:
    '''
    The person detector class.
    This class is responsible for 
    detecting if the person is at upright
    position or lying down
    '''
    def __init__(self) -> None:
        pass

    def detect(self, model_inference, score_thres):
        '''
        Detects if the person is at upright position
        of lying down.

        If the width of the bounding box is higher
        than the height of the bounding box, then 
        the person is lying down. Otherwise they
        are standing or seating
        '''
        # Iterate over each detection
        sum_ratio = 0
        count = 0
        for detection in model_inference[0][0]:
            x1, y1, x2, y2, score = detection
            if score > score_thres:
                width = x2 - x1
                height = y2 - y1
                ratio = width / height
                sum_ratio += ratio
                count += 1

        avg_ratio = sum_ratio / count if count > 0 else 0
        # print(f"Ratio: {avg_ratio}")

        return avg_ratio > 1.5
