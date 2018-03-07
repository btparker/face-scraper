import os
import warnings
import json

class Character(object):
    def __init__(self, name, target_face, character_dir):
        self.name = name
        self.target_face = target_face
        self.character_dir = character_dir
        self.faces_dir = os.path.join(self.character_dir, 'faces/')

    def persist(self):
        # Setting up save directories
        if not os.path.exists(self.character_dir):
            os.makedirs(self.character_dir)
        if not os.path.exists(self.faces_dir):
            os.makedirs(self.faces_dir)

        # Saving target face
        target_face_data = self.add_face(self.target_face)

        # Saving out character data
        data = {
            "name":         self.name,
            "target_face":  target_face_data,
        }

        character_config_path = os.path.join(self.character_dir, "character.json")

        with open(character_config_path, 'w') as outfile:
            json.dump(data, outfile)

    def add_face(self, face):
        faces_config_path = os.path.join(self.character_dir, "faces.json")

        face_data = face.dumps()
        face_filename = "{}.png".format(face.get_hash())
        face_path = os.path.join(
            self.faces_dir,
            face_filename,
        )

        if os.path.exists(face_path):
            print("... face '{}' already exists, skipping".format(face_path))
            return None
        face.save(face_path)
        face_data["path"] = "faces/{}".format(face_filename)

        with open(faces_config_path, "a") as f:
            f.write(json.dumps(face_data)+"\n")

        print("... added '{}' face to '{}'".format(face_data["path"], self.name))

        return face_data

    def load_faces(self):
        faces = []
        faces_config_path = os.path.join(self.character_dir, "faces.json")
        with open(faces_config_path, "rb") as f:
            for line in f:
                face_data = json.loads(line)
                face = self.load_face(self.character_dir, face_data)
                faces.append(face)
        return faces

    @classmethod
    def load_face(self, character_dir, face_data):
        import cv2
        import numpy as np
        from koh.face import Face

        image = cv2.imread(os.path.join(character_dir, face_data["path"]))
        encoding = np.array(face_data["encoding"])
        landmarks = np.array(face_data["landmarks"]).astype("int")

        return Face(image=image, encoding=encoding, landmarks=landmarks)

    @classmethod
    def load(cls, character_dir):
        character_config_path = os.path.join(character_dir, "character.json")
        data = json.load(open(character_config_path, 'rb'))
        target_face_data = data["target_face"]
        target_face = cls.load_face(character_dir, target_face_data)
        return Character(name=data["name"], target_face=target_face, character_dir=character_dir)
