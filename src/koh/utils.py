import numpy as np
import cv2

### MISC ###
def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a

### GEOMETRY ###
def get_bounds_2d(points_2d):
    # Convert to numpy array
    points_2d = np.array(points_2d)

    (x, y) = points_2d.min(axis=0)
    (right, bottom) = points_2d.max(axis=0)

    return (x, y, right, bottom)

def transform_points_2d(points_2d, M):
    ones = np.ones(shape=(len(points_2d), 1))
    points_2d_ones = np.hstack([points_2d, ones])
    points_2d = M.dot(points_2d_ones.T).T
    return points_2d

def get_angle_between_points(point_a, point_b):
    # compute the angle between the eye centroids
    dY = point_b[1] - point_a[1]
    dX = point_b[0] - point_a[0]

    angle = np.degrees(np.arctan2(dY, dX)) - 180
    return angle

def get_center_of_mass(pts, dtype=None):
    pts = np.array(pts)

    if dtype is None:
        dtype = pts.dtype

    return pts.mean(axis=0).astype(dtype)


### CAMERA ###
def get_camera_matrix(frame):
    (h, w) = frame.shape[:2]

    # Camera internals
    focal_length = w
    center = (w/2, h/2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1],
    ], dtype = "double")

    return camera_matrix

def get_camera_distortion():
    # Assuming no lens distortion
    camera_distortion = np.zeros((4,1))
    return camera_distortion


### IMAGE ###

# https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized
