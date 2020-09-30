from flask import Flask, render_template, Blueprint, request, Response, jsonify, make_response
import MySQLdb.cursors
from .validate import validate_user_login

user_login = Blueprint('user_login', __name__, template_folder='templates')
@user_login.route('/login', methods = ['POST'])
def login_user():
    user_email = request.json["email"]
    user_password = request.json["password"]

    user_token = validate_user_login(user_email, user_password)

    print("HELLOHELLO")
    print(user_token)

    if user_token:
        # return jsonify({"jwt_token": user_token})
        return make_response(jsonify({"message": "OK","ok":True,"jwt_token": user_token}), 200)
    else:
        return make_response(jsonify({"message": "","ok":False,"jwt_token": ""}), 400)
