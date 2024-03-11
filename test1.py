from pollinator.camera import Camera
import pollinator.navigation as nav
from pollinator.model import Model
import cv2

c = Camera(0)
c.start_capture()
frame = c.capture()

m = Model("yolov8n-seg.pt")
m.start()
results = m.on(frame)

while True:
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