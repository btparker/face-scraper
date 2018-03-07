from koh.face_models.face_model import FaceModel
from koh.face import Face
import face_recognition
import dlib
import face_recognition_models
import numpy as np
import cv2

FRAME_WIDTH = 512
FACE_SIZE = 256

class HumanFaceModel(FaceModel):

    def __init__(self):
        predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
        self.pose_predictor = dlib.shape_predictor(predictor_68_point_model)

    def face_shape_to_np(self, face_shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)
     
        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coords[i] = (face_shape.part(i).x, face_shape.part(i).y)
     
        # return the list of (x, y)-coordinates
        return coords

    def crop_image_to_landmarks(self, image, landmarks, is_square=True, padding=0.1):
        import math
        from koh.utils import get_bounds_2d

        (x, y, right, bottom) = get_bounds_2d(landmarks)

        # Crop
        fw = right - x
        fh = bottom - y
        fs = max(fw, fh)
        fl_pad = padding * fs + (fs - fw) / 2.0
        fr_pad = padding * fs + (fs - fw) / 2.0
        ft_pad = padding * fs + (fs - fh) / 2.0
        fb_pad = padding * fs + (fs - fh) / 2.0

        x -= fl_pad
        right += fr_pad
        y -= ft_pad
        bottom += fb_pad

        cx = int(round(x))
        cy = int(round(y))
        cright = int(round(right))
        cbottom = int(round(bottom))

        cropped_image = image[cy: cbottom, cx: cright]
        cropped_landmarks = landmarks - np.array([x, y])

        return cropped_image, cropped_landmarks

    def align_image_to_eyeline(self, image, face_landmark):
        from koh.utils import transform_points_2d

        (h, w) = image.shape[:2]
        M = self.get_face_alignment_matrix(image, face_landmark)
        face_landmark = transform_points_2d(face_landmark, M)
        output = cv2.warpAffine(image, M, (w, h))
        return (output, face_landmark)

    def create_face(self, image, face_landmark, face_encoding):
        (
            aligned_face_image,
            aligned_face_landmarks,
        ) = self.align_image_to_eyeline(image, face_landmark)

        (
            cropped_face_image,
            cropped_face_landmarks,
        ) = self.crop_image_to_landmarks(aligned_face_image, aligned_face_landmarks)

        face = Face(
            image=cropped_face_image,
            encoding=face_encoding,
            landmarks=cropped_face_landmarks,
        )

        face.resize(size=FACE_SIZE)
        return face

    def detect_faces(self, frame):
        from koh.utils import image_resize

        # Resize the frame to something sensible if necessary
        scale = 1.0
        fw = frame.shape[1]
        resized_frame = frame

        if fw > FRAME_WIDTH:
            scale = FRAME_WIDTH * 1.0 / fw
            resized_frame = image_resize(image=frame, width=int(fw * scale))

        face_locations = face_recognition.face_locations(resized_frame)
        face_shapes = self._raw_face_landmarks(resized_frame, face_locations)
        face_landmarks = [self.face_shape_to_np(fs) for fs in face_shapes]
        face_encodings = face_recognition.face_encodings(resized_frame)

        face_landmarks = [np.array(fs / scale) for fs in face_landmarks]

        faces = [
            self.create_face(frame, face_landmark, face_encoding) 
            for (face_landmark, face_encoding) in zip(face_landmarks, face_encodings)
        ]

        return faces

    def get_landmarks_group(self, group_key, landmarks):
        from koh.constants import FACIAL_LANDMARKS_IDXS
        (start, end) = FACIAL_LANDMARKS_IDXS[group_key]
        return landmarks[start:end]

    def get_face_alignment_matrix(self, image, face_landmarks):
        from koh.utils import get_angle_between_points
        from koh.utils import get_center_of_mass
        from koh.utils import totuple

        (h, w) = image.shape[:2]
        image_center = np.array([w/2, h/2])

        # extract the left and right eye (x, y)-coordinates
        left_eye_pts = self.get_landmarks_group("left_eye", face_landmarks)
        right_eye_pts = self.get_landmarks_group("right_eye", face_landmarks)

         # compute the center of mass for each eye
        left_eye_center = get_center_of_mass(left_eye_pts)
        right_eye_center = get_center_of_mass(right_eye_pts)
 
        angle = get_angle_between_points(left_eye_center, right_eye_center)

        # compute center (x, y)-coordinates (i.e., the median point)
        # between the two eyes in the input image
        eyes_center = get_center_of_mass([left_eye_center, right_eye_center])

        scale = 1.0
        tX = image_center[0]
        tY = image_center[1]

        eyes_center_tuple = totuple(eyes_center)

        # grab the rotation matrix for rotating and scaling the face
        M = cv2.getRotationMatrix2D(eyes_center_tuple, angle, scale)

        M[0, 2] += (tX - eyes_center[0])
        M[1, 2] += (tY - eyes_center[1])

        return M

    # Copy/Paste (mostly) from private method in face_recognition
    def _raw_face_landmarks(self, face_image, face_locations):
        face_locations = [self._css_to_rect(face_location) for face_location in face_locations]

        return [
            self.pose_predictor(face_image, face_location) 
            for face_location in face_locations
        ]

    def _css_to_rect(self, css):
        return dlib.rectangle(css[3], css[0], css[1], css[2])
    # end of Copy/Paste
