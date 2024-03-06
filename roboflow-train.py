#!pip install roboflow
import os, sys
from roboflow import Roboflow
from ultralytics import YOLO
import config as CONFIG

# params
starting_model = "yolov8s.pt"
epochs = 100
plots = True
yaml_file = "data.yaml"
dataset_format = "yolov8"
roboflow_workspace = "drone-dbsja"
roboflow_project = "flower_dataset-podcd"

# runtime params
args = sys.argv[1:]
if len(args) < 2:
    print("Not enough arguments.")
    exit(99)

# roboflow api key
api_key = CONFIG.ROBOFLOW_API_KEY if args[0] == "null" else args[0]
print("API KEY: " + api_key)

# check version
version = args[1]
try:
    version = int(args[1])
except ValueError:
    print(f"Unable to parse argument for version, got '{version}'")
    exit(1)

device = "cpu"
if len(args) > 2:
    device = args[2]

if len(args) > 3:
    try:
        epochs = int(args[3])
    except ValueError:
        print(f"Unable tp print argument for epochs, got '{args[3]}'")
        exit(1)

# roboflow stuff
rf = Roboflow(api_key=api_key)
project = rf.workspace(roboflow_workspace).project(roboflow_project)
version = project.version(version)

# download version
print("Downloading model...")
dataset = version.download(dataset_format)
print(f"{dataset.name} v{dataset.version} with {dataset.model_format} downloaded at {dataset.location}")

# fix data.yaml
print("Fixing data.yaml...")
import yaml
data_yaml_path = os.path.join(dataset.location, "data.yaml")
data_yaml = yaml.safe_load(open(data_yaml_path, 'r'))
data_yaml['test'] = 'test/images'
data_yaml['train'] = 'train/images'
data_yaml['val'] = 'valid/images'
yaml.dump(data_yaml, open(data_yaml_path, 'w'), default_flow_style=False, allow_unicode=True)
print("...data.yaml fixed")

# train

# if modifying training parameters, change in THIS SECTION
# BEGIN---
print("Beginning training...")
model = YOLO(starting_model)
model.train(
    data=os.path.join(dataset.location, yaml_file),
    plots=plots,
    epochs=epochs,
    device=device)
print("...training complete.")
# ---END

# upload trained model
print("Uploading trained model:")
version.deploy(dataset_format, os.path.join(dataset.location, "runs", "detect", "train"))

# python roboflow-dl.py 14; cd flower_dataset-14; yolo task=detect mode=train model=yolov8s.pt data=$PWD/data.yaml epochs=100 plots=True device=0; cd ../; python roboflow-upload.py 14