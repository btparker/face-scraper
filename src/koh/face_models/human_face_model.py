from koh.face_models.face_model import FaceModel
from koh.face import Face
import face_recognition
import dlib
import face_recognition_models
import numpy as np
import cv2

FRAME_WIDTH = 512

class HumanFaceModel(FaceModel):

    def __init__(self):
        predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
        self.pose_predictor = dlib.shape_predictor(predictor_68_point_model)

    def shape_to_np(self, shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((68, 2), dtype=dtype)
     
        # loop over the 68 facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)
     
        # return the list of (x, y)-coordinates
        return coords

    def crop_image_to_landmarks(self, image, landmarks, is_square=True, padding=0.1):
        import math
        # Crop
        (x, y) = landmarks.min(axis=0)
        (right, bottom) = landmarks.max(axis=0)

        fw = right - x
        fh = bottom - y
        fs = max(fw, fh)
        fl_pad = int(math.floor(padding * fw + (fs - fw) / 2.0))
        fr_pad = int(math.ceil(padding * fw + (fs - fw) / 2.0))
        ft_pad = int(math.floor(padding * fh + (fs - fh) / 2.0))
        fb_pad = int(math.ceil(padding * fh + (fs - fh) / 2.0))

        x -= fl_pad
        right += fr_pad
        y -= ft_pad
        bottom += fb_pad

        cropped_image = image[y: bottom, x: right]
        cropped_landmarks = landmarks - np.array([x, y])

        return cropped_image, cropped_landmarks

    def align_image_to_eyeline(self, image, face_landmark):
        from koh.utils import transform_2d_points

        M = self.get_face_alignment_matrix(face_landmark)
        face_landmark = transform_2d_points(face_landmark, M)
        output = cv2.warpAffine(image, M, image.shape[:2])
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
            cropped_face_image,
            face_encoding,
            cropped_face_landmarks,
        )

        return face

    def detect_faces(self, frame):
        face_locations = face_recognition.face_locations(frame)
        face_shapes = self._raw_face_landmarks(frame, face_locations)
        face_landmarks = [self.shape_to_np(fs) for fs in face_shapes]
        face_encodings = face_recognition.face_encodings(frame)
        faces = [
            self.create_face(frame, face_landmark, face_encoding) 
            for (face_landmark, face_encoding) in zip(face_landmarks, face_encodings)
        ]
        
        return faces

    def get_eye(self, side, face_cropping_landmarks):
        if side != "right" and side != "left":
            raise ValueError("'{}' is not an eye side".format(side))
        
        eye_key = "{}_eye".format(side)
        (start, end) = Face.FACIAL_LANDMARKS_IDXS[eye_key]
        eye_pts = face_cropping_landmarks[start:end]
        return eye_pts

    def get_face_alignment_matrix(self, face_landmarks):
        from koh.utils import get_angle_between_points

        # extract the left and right eye (x, y)-coordinates
        left_eye_pts = self.get_eye("left", face_landmarks)
        right_eye_pts = self.get_eye("right", face_landmarks)

         # compute the center of mass for each eye
        left_eye_center = left_eye_pts.mean(axis=0).astype("int")
        right_eye_center = right_eye_pts.mean(axis=0).astype("int")
 
        angle = get_angle_between_points(left_eye_center, right_eye_center)


        # compute center (x, y)-coordinates (i.e., the median point)
        # between the two eyes in the input image
        eyes_center = ((left_eye_center[0] + right_eye_center[0]) // 2,
            (left_eye_center[1] + right_eye_center[1]) // 2)
 
        scale = 1.0
        # grab the rotation matrix for rotating and scaling the face
        M = cv2.getRotationMatrix2D(eyes_center, angle, scale)

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
