import json


class Skill:
    def __init__(self, existing_skill,  existing_skill_level, desired_skill, desired_skill_level):
        self.existing_skill = existing_skill
        self.existing_skill_level = existing_skill_level
        self.desired_skill = desired_skill
        self.desired_skill_level = desired_skill_level

    def __str__(self):
        return json.dumps(self.__dict__)
