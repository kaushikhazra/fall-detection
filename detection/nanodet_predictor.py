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


class Predictor:
    '''
    The class that encapsulates the NanoDet model.
    This class is inspired from the examples provided
    in NanoDet repository
    '''
    def __init__(self, cfg, model_path, logger, device="cuda:0"):
        '''
        The constructor that configures the neural network
        '''
        self.cfg = cfg
        self.device = device
        # Create the model object
        model = build_model(cfg.model)

        # Load the weights
        ckpt = torch.load(model_path, map_location=lambda storage, loc: storage)
        load_model_weight(model, ckpt, logger)

        # Check if the back bone Re-parameterizable Visual Geometry Group
        # In the configuration I am using it uses ShuffleNetV2, so this
        # condition is always ignored
        if cfg.model.arch.backbone.name == "RepVGG":
            deploy_config = cfg.model
            deploy_config.arch.backbone.update({"deploy": True})
            deploy_model = build_model(deploy_config)
            from nanodet.model.backbone.repvgg import repvgg_det_model_convert

            model = repvgg_det_model_convert(model, deploy_model)

        # Load the model to CPU, I am using Raspberry PI, which does not have
        # a GPU
        self.model = model.to(device).eval()

        # Put the model to detection pipeline provided by NanoDet
        self.pipeline = Pipeline(cfg.data.val.pipeline, cfg.data.val.keep_ratio)

    def inference(self, img):
        '''
        Method that identifies objects
        '''
        # Creating the structure to include the image
        img_info = {"id": 0}
        if isinstance(img, str):
            img_info["file_name"] = os.path.basename(img)
            img = cv2.imread(img)
        else:
            img_info["file_name"] = None
        height, width = img.shape[:2]
        img_info["height"] = height
        img_info["width"] = width
        meta = dict(img_info=img_info, raw_img=img, img=img)

        # Invoke the pipeline on the data
        meta = self.pipeline(None, meta, self.cfg.data.val.input_size)
        meta["img"] = torch.from_numpy(meta["img"].transpose(2, 0, 1)).to(self.device)
        meta = naive_collate([meta])
        meta["img"] = stack_batch_img(meta["img"], divisible=32)

        # The inference block
        with torch.no_grad():
            results = self.model.inference(meta)
        return meta, results

    def visualize(self, dets, meta, class_names, score_thres, wait=0):
        '''
        The method that visualizes the data on the image.
        This method is not used in the detection method, it was just

        '''
        result_img = self.model.head.show_result(
            meta["raw_img"][0], dets, class_names, score_thres=score_thres, show=True
        )
        return result_img