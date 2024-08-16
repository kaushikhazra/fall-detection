class PersonDetector:
    def __init__(self) -> None:
        pass

    def detect(self, model_inference, score_thres):
        # Iterate over each detection for the current class ID
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
