from plumbum import cli
from koh.character import Character
import cv2

class ListFaceDatasetsApp(cli.Application):
    datasets = cli.SwitchAttr(
        ['--datasets'],
        argtype=str,
        mandatory=True,
        help='Path to datasets directory',
    )

    def main(self):
        import os
        import json

        character_ids = [name for name in os.listdir(self.datasets)
            if os.path.isdir(os.path.join(self.datasets, name))]

        for character_id in character_ids:
            character_dir = os.path.join(
                self.datasets,
                character_id,
            )
            character = Character.load(character_dir)
            faces = character.load_faces()
            print("Character '{}', {} faces".format(character.name, len(faces)))

if __name__ == '__main__':
    ListFaceDatasetsApp.run()
