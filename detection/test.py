import os
from DetectionPipeline import DetectionPipeline

if __name__ == '__main__':
    root_folder = 'test-videos/archive/dataset/dataset1'
    files = os.listdir(root_folder)

    for dirpath, dirnames, filenames in os.walk(root_folder):
        for file_name in filenames:
            file_path = os.path.join(dirpath, file_name)
            if os.path.isfile(file_path):
                print("Processing file: " + file_name)
                pipeline = DetectionPipeline(file_path)
                pipeline.start()