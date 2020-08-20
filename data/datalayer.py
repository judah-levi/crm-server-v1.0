from models.student import Student
import json
import os
from data.mongo_datalayer import MongoDataLayer


class DataLayer:

    mongoDB = MongoDataLayer()

    # @staticmethod
    # def add_student(data):
    #     new_student = Student(data["first_name"], data["last_name"], data["email"],
    #                           data["password"], data["existing_skill"], data["existing_skill_level"],
    #                           data["desired_skill"], data["desired_skill_level"])
    #     return new_student

    # @staticmethod
    # def get_student(data):
    #     new_student = Student(data["student_id"], data["first_name"], data["last_name"], data["email"],
    #                           data["password"], data["existing_skill"], data["existing_skill_level"],
    #                           data["desired_skill"], data["desired_skill_level"])
    #     return new_student

    # @staticmethod
    # def load_students():
    #     read_file = "/home/kol/Documents/itc/projects/python/milestones/hogwarts-flask-judah-levi/flask_server/data/" \
    #                 "students.json"
    #     if os.path.exists(read_file):
    #         with open(read_file, "r") as file:
    #             stored_users = json.load(file)
    #             return stored_users

    @staticmethod
    def get_students():
        students = DataLayer.mongoDB.get_all_students()
        return students

    @staticmethod
    def save_student(data):
        students = DataLayer.mongoDB.add_student(data)
        return students

    @staticmethod
    def delete_student(email):
        students = DataLayer.mongoDB.delete_student(email);
        return students

    @staticmethod
    def edit_student(email, data):
        student = DataLayer.mongoDB.edit_student(email, data)
        return student

    @staticmethod
    def get_skill_totals():
        results = DataLayer.mongoDB.count_per_skill()
        return results

    @staticmethod
    def get_des_skill_totals():
        results = DataLayer.mongoDB.count_per_des_skill()
        return results



