import json
import os
import datetime
from dotenv import load_dotenv, find_dotenv
import jwt
from flask import Flask, request, make_response, jsonify, redirect, render_template, session, url_for
from werkzeug.exceptions import HTTPException
from models.student import Student
from data.validators import Validator
from data.datalayer import DataLayer
from data.mongo_datalayer import MongoDataLayer
from lib.decorators import requires_auth

app = Flask(__name__)
app.config['OS_STDOUT'] = os.environ.get("OS_STDOUT")
data_layer = DataLayer()
mongoDB = MongoDataLayer()

@app.route("/login", methods=['POST'])
def login_user():
    auth = request.authorization
    user_name = auth.username
    password = auth.password
    check_user = mongoDB.login(user_name, password)
    if check_user["authenticated"]:
        token = jwt.encode({'user': check_user, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(days=2)}, app.config['OS_STDOUT'], 'HS256')
        return jsonify({'token': token.decode('UTF-8')})
    return make_response(jsonify({"message": 'login failed'}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route("/signup", methods=["POST"])
@requires_auth
def user_signup():
    try:
        request_body = request.get_json()
        user_name = request_body["user_name"]
        password = request_body["password"]
        email = request_body["email"]
        if mongoDB.user_lookup(email) is not True:
            new_user = mongoDB.signup(user_name, password, email)
            token = jwt.encode({'user': new_user, 'exp': datetime.datetime.utcnow(
            ) + datetime.timedelta(days=2)}, app.config['OS_STDOUT'], 'HS256')
            return jsonify({'token': token.decode('UTF-8')})
        else:
            return make_response(jsonify({"message": "User already Exists"}), 409)
    except KeyError:
        return make_response(jsonify({"message": "missing fields"}), 409)

@app.route("/dashboard")
@requires_auth
def get_all_students():
    students = data_layer.get_students()
    resp = app.response_class(response=json.dumps({"students": students}),
                              status=200,
                              mimetype='application/json')
    return resp

@app.route("/students/<email>")
@requires_auth
def get_student_by_email(email):
    query = mongoDB.get_student_by_email(email)
    if query:
        return app.response_class(response=json.dumps(query),
                                  status=200,
                                  mimetype='application/json')
    else:
        return make_response(jsonify({"message": "Student doesn't Exist"}), 400)

@app.route("/students/skills/desired_skill_total")
@requires_auth
def get_count_per_des_skill():
    results = data_layer.get_des_skill_totals()
    resp = app.response_class(response=json.dumps({"desired skills": results}),
                              status=200,
                              mimetype='application/json')
    return resp

@app.route("/students/skills/existing_skill_total")
@requires_auth
def get_count_per_skill():
    results = data_layer.get_skill_totals()
    resp = app.response_class(response=json.dumps({"existing skills": results}),
                              status=200,
                              mimetype='application/json')
    return resp

@app.route("/students/add", methods=['POST'])
@requires_auth
def add_new_student():
    data = request.get_json()
    Validator.validate_new_student(data)
    new_student = data_layer.save_student(data)
    return new_student

@app.route("/students/edit/<email>", methods=['PUT'])
@requires_auth
def edit_student(email):
    data = request.get_json()
    Validator.validate_new_student(data)
    edited_student = data_layer.edit_student(email, data)
    return edited_student

@app.route("/students/delete/<email>", methods=['DELETE'])
@requires_auth
def delete_student(email):
    data_layer.delete_student(email)
    return make_response(jsonify({"message": "Student deleted Successfully"}), 200)


if __name__ == '__main__':
    if os.environ.get('PORT') is not None:
        app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT'))
    else:
        app.run(debug=True, host='0.0.0.0') 