import os
import warnings


class Character(object):
    def __init__(self, name, target_face, output):

        character_id = name.replace(' ', '_').lower()

        character_output = os.path.join(output, character_id)
        faces_output = os.path.join(character_output, 'faces/')

        if os.path.exists(character_output):
            warnings.warn('Person ID "{}" exists at "{}"'.format(
                character_id,
                character_output,
            ))
        else:
            os.makedirs(character_output)
            os.makedirs(faces_output)

        self.name = name
        self.character_id = character_id
        self.target_face = target_face
        self.character_output = character_output
        self.faces_output = faces_output

        self.character_config_path = os.path.join(self.character_output, "character.json")
        self.save()

    def dumps(self):
        target_face_data = self.target_face.dumps()
        target_face_filename = "{}.png".format(self.target_face.get_hash())
        target_face_path = os.path.join(
            self.faces_output,
            target_face_filename,
        )

        self.target_face.save(target_face_path)
        target_face_data["path"] = "faces/{}".format(target_face_filename)
        return {
            "name":         self.name,
            "character_id": self.character_id,
            "target_face":  target_face_data,
        }

    def save(self):
        import json
        with open(self.character_config_path, 'w') as outfile:
            json.dump(self.dumps(), outfile)


