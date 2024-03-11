import cv2

class Camera:
    def __init__(self, camera_id, width = None, height = None):
        self.first = True
        self.camera_id = camera_id

        self.video_capture = None
        self.frame = None
        self.video_width = width
        self.video_height = height

    def start_capture(self):
        self.video_capture = cv2.VideoCapture(self.camera_id)

        if self.video_width is not None:
            self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.video_width)
        else:
            self.video_width = self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)

        if self.video_height is not None:
            self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.video_height)
        else:
            self.video_height = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

        print(f"Initiated capture on {self.camera_id} at {self.video_width}w x {self.video_height}h @ {self.video_capture.get(cv2.CAP_PROP_FPS)}")
        return self.video_capture

    def capture(self):
        if self.video_capture is None:
            raise RuntimeError("No camera initiated! Run Camera.start_capture() first!")

        _, self.frame = self.video_capture.read()
        while not self.frame:
            print("Retrying capture, no initial frame was found from capture.")
            _, self.frame = self.video_capture.read()
        self.frame = self.frame.copy()

        if self.first:
            self.first = False

        return self.frame

    def show_capture(self, _window = None):
        if (self.video_capture is None) or (self.frame is None):
            raise RuntimeError("No capture or frame in Camera! Run Camera.capture() first!")
        if _window is None:
            _window = f"Frame: {self.video_width}w x {self.video_height}h {self.video_capture.get(cv2.CAP_PROP_FPS)}f"
        cv2.imshow(_window, self.frame)
        print("Image is shown.")
        cv2.waitKey(0)

    def init(self):
        self.start_capture()
        self.capture()
        self.show_capture()
