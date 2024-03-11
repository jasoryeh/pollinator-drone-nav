import unittest

import numpy as np

import pollinator.model as model
import cv2
import numpy

class TestModel(unittest.TestCase):

    def test_working(self):
        modelname = "yolov8n-seg.pt"
        m = model.Model(modelname)
        self.assertEqual(m.model_name, modelname)
        m.start()
        self.assertIsNotNone(m.model)
        blank_frame = numpy.zeros((1080, 1920, 3), numpy.uint8)
        self.assertIsNotNone(blank_frame)
        results = m.on(blank_frame)
        self.assertIsNotNone(results)
        detections = m.parse_detections(results)
        self.assertEqual(len(detections), 0)
        #m.show_results(results)

if __name__ == '__main__':
    unittest.main()