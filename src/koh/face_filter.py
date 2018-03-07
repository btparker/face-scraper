class FaceFilter(object):
    def __init__(self, face, threshold = 0.6):
        self.encoding = face.encoding
        self.threshold = threshold
    
    def check(self, face_image):
        encodings = face_recognition.face_encodings(face_image)
        score = face_recognition.face_distance([self.encoding], encodings)
        return score <= self.threshold
