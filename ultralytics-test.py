from ultralytics import YOLO
import cv2
import multiprocessing

# Configuration - Change this to make things work locally
CAMERAID = 1

# "yolov8x-cls.pt" # classification only - xl sized
# "yolov8x.pt" # detect only - xl
# "yolov8x-seg.pt" # segmentation only - xl
# "yolov8n-seg.pt" # segmentation only (nano pretrained model)
YOLO_MODEL = "yolov8x-seg.pt"

oldprint = print
def print(*args, **kwargs):
    if True:
        oldprint(*args, **kwargs)

def execute_model(model, frame):
    results = model(frame)[0]
    detections = []
    for result in results:
        print(f"Result")
        for box in result.boxes:
            print(f"    Box:")
            print(f"        Confidence: {box.conf}")
            print(f"        Type ID: {box.cls}")
            print(f"        Type: {result.names[box.cls[0].item()]}")
            print(f"        Bounds: {box.xyxy}")
            print(f"    Box end")

            # draw details on frame over
            bounds = box.xyxy[0]
            x1, y1 = (int(bounds[0].item()), int(bounds[1].item()))
            x2, y2 = (int(bounds[2].item()), int(bounds[3].item()))
            
            detections.append([result.names[box.cls[0].item()], box.conf[0].item(), (x1, y1), (x2, y2), (255, 0, 0), 1])
            # name, confidence, p1, p2, color, thick
        print(f"Result end")
    cv2.imshow('processing', results.plot())
    cv2.waitKey(1)
    print(f"Detections: {len(detections)}")
    return detections


def run_model(q_tohere: multiprocessing.Queue, q_toparent: multiprocessing.Queue):
    global _detections
    # Load a model
    print("Load model...")
    model = YOLO(YOLO_MODEL)
    print("Load model done.")

    # Use the model
    print("Run...")
    while True:
        frame = q_tohere.get()
        dets = execute_model(model, frame)
        q_toparent.put(dets)

def run_cam(q_in: multiprocessing.Queue, q_out: multiprocessing.Queue):
    print("Cam...")

    first = True
    detections = []
    # cam capture
    capture = cv2.VideoCapture(CAMERAID)
    #capture.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    #capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 100)
    while True:
        ret, frame = capture.read()

        if first:
            q_out.put(frame.copy())
            first = False

        if not q_in.empty():
            q_out.put(frame.copy())
            detections = q_in.get()
        

        #print("ADetections: " + str(len(detections)))
        for detection in detections:
            name, confidence, p1, p2, color, thick = detection
            cv2.rectangle(frame, p1, p2, color=color, thickness=thick)
            cv2.putText(frame, f"{name} {confidence}", (p1[0], p1[1]+12), fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=color)

        cv2.imshow('image', frame)
        cv2.waitKey(1)
        #print("Cam done.")



if __name__ == '__main__':
    queue_tohere = multiprocessing.Queue() # read data to use from this
    queue_toprocess = multiprocessing.Queue() # write data to process using this

    p1 = multiprocessing.Process(target=run_model, args=(queue_toprocess, queue_tohere))
    p2 = multiprocessing.Process(target=run_cam, args=(queue_tohere, queue_toprocess))
    p1.start()
    p2.start()

    while True:
        pass