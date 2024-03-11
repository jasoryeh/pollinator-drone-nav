from ultralytics import YOLO
import cv2
import multiprocessing
import pollinator.navigation as nav

# Configuration - Change this to make things work locally
CAMERAID = 2

# "yolov8x-cls.pt" # classification only - xl sized
# "yolov8x.pt" # detect only - xl
# "yolov8x-seg.pt" # segmentation only - xl
# "yolov8n-seg.pt" # segmentation only (nano pretrained model)
YOLO_MODEL = "yolov8n-seg.pt"
#YOLO_MODEL = "b2best.pt"

# tuple (width, height), None for none
#CAPTURE_LIMITS = (300, 200)
CAPTURE_LIMITS = None


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
            # draw details on frame over
            bounds = box.xyxy[0]
            x1, y1 = (int(bounds[0].item()), int(bounds[1].item()))
            x2, y2 = (int(bounds[2].item()), int(bounds[3].item()))

            move = nav.calculate_move_bounds((len(frame[0]), len(frame)), (x1, y1, x2, y2))
            print(f"    Box:")
            print(f"        Confidence: {box.conf}")
            print(f"        Type ID: {box.cls}")
            print(f"        Type: {result.names[box.cls[0].item()]}")
            print(f"        Bounds: {box.xyxy}")
            print(f"        Move: {move}")
            print(f"    Box end")

            processed = [result.names[box.cls[0].item()], box.conf[0].item(), (x1, y1), (x2, y2), (255, 0, 0), 1, move]
            detections.append(processed)
            # name, confidence, p1, p2, color, thick, move
        print(f"Result end")
    cv2.imshow('processing', results.plot())
    cv2.waitKey(1)
    print(f"Detections: {len(detections)}")
    return detections


def run_model(q_tohere: multiprocessing.Queue, q_toparent: multiprocessing.Queue):
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
    capture = cv2.VideoCapture(CAMERAID)
    if not (CAPTURE_LIMITS is None):
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, CAPTURE_LIMITS[0])
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, CAPTURE_LIMITS[1])
    
    while True:
        _, frame = capture.read()

        if first:
            q_out.put(frame.copy())
            first = False

        if not q_in.empty():
            q_out.put(frame.copy())
            detections = q_in.get()
        

        #print("ADetections: " + str(len(detections)))
        for detection in detections:
            name, confidence, p1, p2, color, thick, move = detection
            cv2.rectangle(frame, p1, p2, color=color, thickness=thick)
            cv2.putText(frame, f"{name} {confidence:.2f} {str(move)}", (p1[0], p1[1]+12), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1.2, color=color)

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