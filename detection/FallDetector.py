import torch
from nanodet_predictor import Predictor
from person_detector import PersonDetector
from nanodet.util import cfg, load_config, Logger

class FallDetector:
    def __init__(self, config_path='nanodet_m.yml', model_path='nanodet_m.ckpt', score_threshold=0.35):
        self.predictor = None
        self.detector = None
        self.config_path = config_path
        self.model_path = model_path
        self.score_threshold = score_threshold

    def initialize_predictor(self):
        # Load configuration and initialize the predictor
        load_config(cfg, self.config_path)
        logger = Logger(-1, use_tensorboard=False)
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.predictor = Predictor(cfg, self.model_path, logger, device=device)

    def initialize_detector(self):
        # Initialize the person detector
        self.detector = PersonDetector()

    def detect_fall(self, frame):
        # Initialize predictor if not already initialized
        if self.predictor is None:
            self.initialize_predictor()

        # Initialize detector if not already initialized
        if self.detector is None:
            self.initialize_detector()

        # Perform inference on the frame
        meta, res = self.predictor.inference(frame)

        # Detect if a fall has occurred based on the inference results
        fall_detected = self.detector.detect(res, self.score_threshold)

        return fall_detected