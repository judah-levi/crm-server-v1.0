import json
from models.skill import Skill
import datetime
import random

# student_string = '{"student_id": "12312", "first_name": "Harry", "last_name": "Potter", "email":"hp@gmail.com", ' \
#                  '"password":"123123", "creation_time":"2020/14/07", "last_update":"2020/14/07 19:34", ' \
#                  '"existing_skill":"potions", "existing_skill_level": 3, ' \
#                  '"desired_skill":"defense against the dark arts", "desired_skill_level":"1"}'


class Student(Skill):
    def __init__(self, first_name, last_name, email, password, existing_skill,
                 existing_skill_level, desired_skill, desired_skill_level):
        # self.student_id = random.randint(1, 100000)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.creation_time = datetime.datetime.now().strftime("%Y_%m_%d, %H:%M:%S")
        self.last_update = self.creation_time
        super().__init__(existing_skill, existing_skill_level, desired_skill, desired_skill_level)

    def __str__(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, string):
        student_dict = json.loads(string)
        new_student = Student(**student_dict)
        print(student_dict)
        print(new_student)
        return new_student


# Student.from_json(student_string)

