from plumbum import cli
from koh.face_models.human_face_model import HumanFaceModel
from koh.character import Character
import cv2

class CreateFaceDatasetApp(cli.Application):
    image_path = cli.SwitchAttr(
        ['--image'],
        argtype=str,
        mandatory=True,
        help='Image to initialize facial identity',
    )

    name = cli.SwitchAttr(
        ['--name'],
        argtype=str,
        mandatory=True,
        help='Name of the identity',
    )

    data_output = cli.SwitchAttr(
        ['--datasets'],
        argtype=str,
        mandatory=True,
        help='Path to output datasets',
    )

    def main(self):
        import os
        import json

        frame = cv2.imread(self.image_path)
        face_model = HumanFaceModel()
        faces = face_model.detect_faces(frame=frame)

        if len(faces) != 1:
            raise ValueError('{} faces detected in image "{}", should be 1'.format(
                len(faces),
                self.image_path
            ))

        face = faces[0]
        character_id = self.name.replace(' ', '_').lower()
        character_output = os.path.join(self.data_output, character_id)
        character = Character(name=self.name, target_face=face, character_dir=character_output)
        character.persist()

if __name__ == '__main__':
    CreateFaceDatasetApp.run()
