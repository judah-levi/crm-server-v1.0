import pymongo
import os
from argon2 import PasswordHasher

client = pymongo.MongoClient(os.environ.get("DB_URI"))
db = client["crm_dev"]
user_collection = db["users"]
student_data = db["data"]
ph = PasswordHasher()

class MongoDataLayer:

    @staticmethod
    def signup(user_name, password, email):
        hashed_password = ph.hash(password)
        user_collection.insert_one({
            "user": user_name,
            "password": hashed_password,
            "email": email})
        return str(user_collection.find_one({'user': user_name})["_id"])

    @staticmethod
    def login(user_name, password):
        find_user = user_collection.find_one({'user': user_name})
        if ph.verify(find_user["password"], password):
            return {"user_id": str(find_user["_id"]), "authenticated": True}
        else:
            return {"authenticated": False}

    @staticmethod
    def get_all_students():
        students_dict = {}
        students = list(student_data.find())
        for student in students:
            students_dict[student["email"]] = {
                "id": str(student["_id"]),
                "first_name": student["first_name"],
                "last_name": student["last_name"],
                "email": student["email"],
                "existing_skill": student["existing_skill"],
                "existing_skill_level": student["existing_skill_level"],
                "desired_skill": student["desired_skill"],
                "desired_skill_level": student["desired_skill_level"]
            }
        return students_dict
    
    @staticmethod
    def get_student_by_email(email):
        students_dict = {}
        student = student_data.find_one({"email": email})
        if student:
            students_dict[student["email"]] = {
                "id": str(student["_id"]),
                "first_name": student["first_name"],
                "last_name": student["last_name"],
                "email": student["email"],
                "existing_skill": student["existing_skill"],
                "existing_skill_level": student["existing_skill_level"],
                "desired_skill": student["desired_skill"],
                "desired_skill_level": student["desired_skill_level"]
            }
            return students_dict
        else: 
            return False
    

    @staticmethod
    def add_student(data):
        student_data.insert_one(data)
        return "New student added successfully!"

    @staticmethod
    def edit_student(email, data):
        student_data.update({"email": email}, data)
        return "Student edited successfully!"

    @staticmethod
    def delete_student(email):
        student_data.remove({"email": email})
        return "Student deleted successfully"

    @staticmethod
    def count_per_skill():
        results_dict = {}
        results = student_data.aggregate([{"$group": {"_id": "$existing_skill", "count": {"$sum": 1}}}])
        for result in results:
            results_dict[result["_id"]] = {
                "id": result["_id"],
                "count": result["count"]
            }
        return results_dict

    @staticmethod
    def count_per_des_skill():
        results_dict = {}
        results = student_data.aggregate([{"$group": {"_id": "$desired_skill", "count": {"$sum": 1}}}])
        for result in results:
            results_dict[result["_id"]] = {
                "id": result["_id"],
                "count": result["count"]
            }
        return results_dict

    @staticmethod
    def user_lookup(email):
        if user_collection.find_one({"email": email}):
            return True
        else:
            return False

