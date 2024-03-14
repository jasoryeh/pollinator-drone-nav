import cv2
from ultralytics import YOLO
from picamera2 import Picamera2
import numpy
from PIL import Image

#specify the YOLO model we are gonna use
model = YOLO('yolov8n.pt')


#process the frame with ultralytics
def process(frame:numpy.ndarray):
    results = model(frame)

#show the inference with opencv
def display():
    pass


#start the PiCamera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1000, 480)}))
picam2.start()
while True:

    im = picam2.capture_array() #im is a numpy array
    print(im.shape)
    im = im[:,:,:3] #slicing the array to remove the alpha channel
    process(im)
    #cv2.imshow('HELLO',im)
    #cv2.waitKey(1)
     
        



'''while True:
    for result in results:
        boxes = result.boxes
        probs = result.probs'''
        


