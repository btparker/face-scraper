from plumbum import cli
from koh.character import Character
from koh.face_models.human_face_model import HumanFaceModel
import cv2
import face_recognition

class ExtractFacesApp(cli.Application):
    character = cli.SwitchAttr(
        ['--character'],
        argtype=str,
        list=True,
        mandatory=True,
        help='Path to character directory',
    )

    image_path = cli.SwitchAttr(
        ['--image'],
        argtype=str,
        default=None,
        excludes=['--video'],
        help='Image to initialize facial identity',
    )

    video_path = cli.SwitchAttr(
        ['--video'],
        argtype=str,
        default=None,
        excludes=['--image'],
        help='Image to initialize facial identity',
    )

    def process_frame(self, frame, frame_id, characters, face_model):
        faces = face_model.detect_faces(frame=frame)
        print("Found {} faces in frame {}".format(len(faces), frame_id))
        for face in faces:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(
                [character.target_face.encoding for character in characters],
                face.encoding,
            )
            
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                character = characters[first_match_index]
                print("Face matched {}, adding...".format(character.name))
                character.add_face(face)

    def process_video(self, video, characters, face_model, frame_step):
        while(video.isOpened()):
            success, frame = video.read()
            frame_idx = int(video.get(1) - 1)

            if success:
                if frame_idx % frame_step != 0:
                    continue

                self.process_frame(
                    frame=frame,
                    frame_id=frame_idx,
                    characters=characters,
                    face_model=face_model,
                )
            else:
                break

    def main(self):
        import os
        import json

        face_model = HumanFaceModel()

        characters = [Character.load(char_dir) for char_dir in self.character]
        for character in characters:
            print("Checking for character '{}'".format(character.name))

        if self.image_path is not None:
            frame = cv2.imread(self.image_path)
            self.process_frame(frame, self.image_path, characters, face_model)
        elif self.video_path is not None:
            video = cv2.VideoCapture(self.video_path)
            self.process_video(video, characters, face_model, 5)

if __name__ == '__main__':
    ExtractFacesApp.run()
