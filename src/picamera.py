
from pickle import TRUE
import picamera
import time

def capture_image(image_path):
    with picamera.PiCamera() as camera:
        camera.resolution = (1024, 768)
        camera.start_preview()
        # sleeping for 2 ms, make sure though its ms though
        time.sleep(2)
        camera.capture(image_path)
        print(f"\33[1;31mImage captured and saved at {image_path}\33[0m")

if __name__ == '__picamera__': 
    framenum = 0
    while TRUE:
        capture_image('/home/pi/captured_image%s.jpg'%framenum)
        framenum+=1