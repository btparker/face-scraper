import numpy as np
import cv2
from collections import OrderedDict

class Face(object):

    FACIAL_LANDMARKS_IDXS = OrderedDict([
        ("mouth", (48, 68)),
        ("right_eyebrow", (17, 22)),
        ("left_eyebrow", (22, 27)),
        ("right_eye", (36, 42)),
        ("left_eye", (42, 48)),
        ("nose", (27, 36)),
        ("jaw", (0, 17))
    ])

    def __init__(self, image, encoding, landmarks):
        self.image = image
        self.landmarks = landmarks
        self.encoding = encoding

    def get_image(self, size=None):
        return self.image.copy()

    def get_hash(self):
        import hashlib
        import json
        m = hashlib.md5()
        m.update(json.dumps(self.dumps()))
        return m.hexdigest()

    def show(self, show_landmarks=True):
        image = self.get_image().copy()
        if show_landmarks:
            for (x, y) in self.landmarks:
                cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
        cv2.imshow("face", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save(self, path, show_landmarks=False):
        image = self.get_image()
        if show_landmarks:
            for (x, y) in self.landmarks:
                cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
        cv2.imwrite(path, image)

    def resize(self, size):
        (h, w, _) = self.image.shape
        sy = size * 1.0 / h
        sx = size * 1.0 / w
        self.landmarks = self.landmarks * np.array([sx, sy])
        self.landmarks = self.landmarks.astype("int")
        self.image = cv2.resize(self.image, (size, size))\

    def dumps(self):
        return {
            "landmarks":    self.landmarks.tolist(),
            "encoding":     self.encoding.tolist(),
        }
