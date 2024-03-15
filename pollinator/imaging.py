import cv2
import camera as camera
class Imager:
    def __init__(self):
        self.collection = []

        self.stitcher = None

    def capture(self, cam: camera.Camera):
        cap = cam.capture()
        self.collection.append(cap)
        return cap

    def add(self, img):
        self.collection.append(img)

    def merge(self):
        if self.stitcher is None:
            self.stitcher = cv2.Stitcher.create()
        result, comb = self.stitcher.stitch(self.collection)
        return comb if result == cv2.STITCHER_OK else None



if __name__ == "__main__":
    imgr = Imager()
    cam = camera.Camera(2)
    cam.start_capture()

    while input("capture") != 'n':
        cap = cam.capture()
        imgr.add(cap)
        cv2.imshow("captured", cap)
        cv2.waitKey(0)
        input('press any key to continue')

        merged = imgr.merge()
        if merged is None:
            print("Not enough to stitch current captures")
            continue
        cv2.imshow("after stitching", merged)
        input('press any key to go')
        cv2.waitKey(0)
