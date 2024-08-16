import argparse
import cv2
import torch
import numpy as np
from nanodet.util import cfg, load_config, Logger
from nanodet.model.arch import build_model
from nanodet.util import load_model_weight
from nanodet.data.batch_process import stack_batch_img
from nanodet.data.collate import naive_collate
from nanodet.data.transform import Pipeline

from nanodet_predictor import Predictor
from person_detector import PersonDetector


def main():
    config_path = 'nanodet_m.yml'
    model_path = 'nanodet_m.ckpt'
    load_config(cfg, config_path)
    logger = Logger(-1, use_tensorboard=False)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    predictor = Predictor(cfg, model_path, logger, device=device)
    detector = PersonDetector()

    test_video = "../test-videos/fall/cam7.avi"
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture(test_video)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    score_thres = 0.35
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        meta, res = predictor.inference(frame)
        result_frame = predictor.visualize(res[0], meta, cfg.class_names, score_thres)

        fall_detectec = detector.detect(res, score_thres)

        if fall_detectec:
            print("Fall Detected : YES")
        else:
            print("Fall Detected : NO ")

        cv2.imshow('NanoDet Object Detection', result_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
