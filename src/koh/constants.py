from collections import OrderedDict
import numpy as np

FACIAL_LANDMARKS_IDXS = {
    "mouth": (48, 68),
    "right_eyebrow": (17, 22),
    "left_eyebrow": (22, 27),
    "right_eye": (36, 42),
    "left_eye": (42, 48),
    "nose": (27, 36),
    "jaw": (0, 17),
    "right_side": (0),
    "gonion_right": (4),
    "menton": (8),
    "gonion_left": (12),
    "left_side": (16),
    "frontal_breadth_right": (17),
    "frontal_breadth_left": (26),
    "sellion": (27),
    "nose": (30),
    "sub_nose": (33),
    "right_eye_outer": (36),
    "right_eye_inner": (39),
    "left_eye_inner": (42),
    "left_eye_outer": (45),
    "lip_right": (48),
    "lip_left": (54),
    "stomion": (62),
}

TRACKED_FACIAL_LANDMARKS = [
    FACIAL_LANDMARKS_IDXS["right_side"],
    FACIAL_LANDMARKS_IDXS["gonion_right"],
    FACIAL_LANDMARKS_IDXS["menton"],
    FACIAL_LANDMARKS_IDXS["gonion_left"],
    FACIAL_LANDMARKS_IDXS["left_side"],
    FACIAL_LANDMARKS_IDXS["frontal_breadth_right"],
    FACIAL_LANDMARKS_IDXS["frontal_breadth_left"],
    FACIAL_LANDMARKS_IDXS["sellion"],
    FACIAL_LANDMARKS_IDXS["nose"],
    FACIAL_LANDMARKS_IDXS["sub_nose"],
    FACIAL_LANDMARKS_IDXS["right_eye_outer"],
    FACIAL_LANDMARKS_IDXS["right_eye_inner"],
    FACIAL_LANDMARKS_IDXS["left_eye_inner"],
    FACIAL_LANDMARKS_IDXS["left_eye_outer"],
    # FACIAL_LANDMARKS_IDXS["lip_right"],
    # FACIAL_LANDMARKS_IDXS["lip_left"],
    FACIAL_LANDMARKS_IDXS["stomion"],
]

#Antropometric constant values of the human head. 
#Found on wikipedia and on:
# "Head-and-Face Anthropometric Survey of U.S. Respirator Users"
#
#X-Y-Z with X pointing forward and Y on the left.
#The X-Y-Z coordinates used are like the standard
# coordinates of ROS (robotic operative system)
FACIAL_3D_LANDMARKS_MAPPING = {
    "right_side": np.float32([-100.0, -77.5, -5.0]), #0
    "gonion_right": np.float32([-110.0, -77.5, -85.0]), #4
    "menton": np.float32([0.0, 0.0, -122.7]), #8
    "gonion_left": np.float32([-110.0, 77.5, -85.0]), #12
    "left_side": np.float32([-100.0, 77.5, -5.0]), #16
    "frontal_breadth_right": np.float32([-20.0, -56.1, 10.0]), #17
    "frontal_breadth_left": np.float32([-20.0, 56.1, 10.0]), #26
    "sellion": np.float32([0.0, 0.0, 0.0]), #27
    "nose": np.float32([21.1, 0.0, -48.0]), #30
    "sub_nose": np.float32([5.0, 0.0, -52.0]), #33
    "right_eye_outer": np.float32([-20.0, -65.5,-5.0]), #36
    "right_eye_inner": np.float32([-10.0, -40.5,-5.0]), #39
    "left_eye_inner": np.float32([-10.0, 40.5,-5.0]), #42
    "left_eye_outer": np.float32([-20.0, 65.5,-5.0]), #45
    # "lip_right": np.float32([-20.0, 65.5,-5.0]), #48
    # "lip_left": np.float32([-20.0, 65.5,-5.0]), #54
    "stomion": np.float32([10.0, 0.0, -75.0]), #62
}

FACIAL_3D_LANDMARKS = np.float32([
    FACIAL_3D_LANDMARKS_MAPPING["right_side"],
    FACIAL_3D_LANDMARKS_MAPPING["gonion_right"],
    FACIAL_3D_LANDMARKS_MAPPING["menton"],
    FACIAL_3D_LANDMARKS_MAPPING["gonion_left"],
    FACIAL_3D_LANDMARKS_MAPPING["left_side"],
    FACIAL_3D_LANDMARKS_MAPPING["frontal_breadth_right"],
    FACIAL_3D_LANDMARKS_MAPPING["frontal_breadth_left"],
    FACIAL_3D_LANDMARKS_MAPPING["sellion"],
    FACIAL_3D_LANDMARKS_MAPPING["nose"],
    FACIAL_3D_LANDMARKS_MAPPING["sub_nose"],
    FACIAL_3D_LANDMARKS_MAPPING["right_eye_outer"],
    FACIAL_3D_LANDMARKS_MAPPING["right_eye_inner"],
    FACIAL_3D_LANDMARKS_MAPPING["left_eye_inner"],
    FACIAL_3D_LANDMARKS_MAPPING["left_eye_outer"],
    FACIAL_3D_LANDMARKS_MAPPING["stomion"],
])
