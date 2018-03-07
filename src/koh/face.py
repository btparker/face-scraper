import numpy as np
import cv2

class Face(object):

    def __init__(self, image, encoding, landmarks):
        self.image = image
        self.landmarks = landmarks
        self.encoding = encoding
        self.pose = self.compute_pose(image=image, landmarks_2d=landmarks)

    def get_image(self, size=None):
        return self.image.copy()

    def get_hash(self):
        import hashlib
        import json
        m = hashlib.md5()
        m.update(json.dumps(self.dumps()))
        return m.hexdigest()

    def show(self, draw_landmarks=False, draw_pose=False):
        image = self.get_image().copy()
        if draw_landmarks:
            self.draw_landmarks(image)
        if draw_pose:
            self.draw_pose(image)
        cv2.imshow("face", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def save(self, path, draw_landmarks=False, draw_pose=False):
        image = self.get_image()
        if draw_landmarks:
            self.draw_landmarks(image)
        if draw_pose:
            self.draw_pose(image)
            
        cv2.imwrite(path, image)

    def draw_landmarks(self, image):
        for (x, y) in self.landmarks:
            x = int(round(x))
            y = int(round(y))
            cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
        return image

    def draw_pose(self, image):
        from koh.utils import get_camera_matrix
        from koh.utils import get_camera_distortion
        from koh.constants import TRACKED_FACIAL_LANDMARKS

        tracked_landmarks_2d = self.landmarks[TRACKED_FACIAL_LANDMARKS]
        tracked_landmarks_2d = tracked_landmarks_2d.astype("int")
        camera_matrix = get_camera_matrix(frame=image)
        camera_distortion = get_camera_distortion()

        #Now we project the 3D points into the image plane
        #Creating a 3-axis to be used as reference in the image.
        axis = np.float32([
            [50,0,0], 
            [0,50,0], 
            [0,0,50],
        ])

        imgpts, jac = cv2.projectPoints(
            axis,
            self.pose["rotation"],
            self.pose["translation"],
            camera_matrix,
            camera_distortion,
        )

        #Drawing the three axis on the image frame.
        #The opencv colors are defined as BGR colors such as: 
        # (a, b, c) >> Blue = a, Green = b and Red = c
        #Our axis/color convention is X=R, Y=G, Z=B
        sellion_xy = (tracked_landmarks_2d[7][0], tracked_landmarks_2d[7][1])
        cv2.line(image, sellion_xy, tuple(imgpts[1].ravel()), (0,255,0), 3) #GREEN
        cv2.line(image, sellion_xy, tuple(imgpts[2].ravel()), (255,0,0), 3) #BLUE
        cv2.line(image, sellion_xy, tuple(imgpts[0].ravel()), (0,0,255), 3) #RED
        return image

    def resize(self, size):
        (h, w, _) = self.image.shape
        sy = size * 1.0 / h
        sx = size * 1.0 / w
        self.landmarks = self.landmarks * np.array([sx, sy])
        self.landmarks = self.landmarks.astype("int")
        self.image = cv2.resize(self.image, (size, size))


    @classmethod
    def compute_pose(cls, image, landmarks_2d):
        from koh.utils import get_camera_matrix
        from koh.utils import get_camera_distortion
        from koh.constants import FACIAL_3D_LANDMARKS
        from koh.constants import TRACKED_FACIAL_LANDMARKS

        camera_matrix = get_camera_matrix(frame=image)
        camera_distortion = get_camera_distortion()

        # Get the "important" landmarks
        tracked_landmarks_2d = landmarks_2d[TRACKED_FACIAL_LANDMARKS]

        # Convert to same dtype as our 3D landmarks
        tracked_landmarks_2d = tracked_landmarks_2d.astype(FACIAL_3D_LANDMARKS.dtype)

        (
            success,
            rotation_vector,
            translation_vector,
        ) = cv2.solvePnP(
            objectPoints=FACIAL_3D_LANDMARKS,
            imagePoints=tracked_landmarks_2d,
            cameraMatrix=camera_matrix,
            distCoeffs=camera_distortion,
            flags=cv2.SOLVEPNP_ITERATIVE,
        )

        pose = {
            "translation": translation_vector,
            "rotation": rotation_vector,
        }

        return pose


    def dumps(self):
        return {
            "landmarks": self.landmarks.tolist(),
            "encoding": self.encoding.tolist(),
            "pose": {
                "translation": self.pose["translation"].tolist(),
                "rotation": self.pose["rotation"].tolist(),
            }
        }
