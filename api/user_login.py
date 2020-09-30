from flask import Flask, render_template, Blueprint, request, Response, jsonify
import MySQLdb.cursors
from .validate import validate_user_login

user_login = Blueprint('user_login', __name__, template_folder='templates')
@user_login.route('/login', methods = ['GET'])
def login_user():
    user_email = request.json["email"]
    user_password = request.json["password"]

    user_token = validate_user_login(user_email, user_password)

    print("HELLOHELLO")
    print(user_token)

    if user_token:
        return jsonify({"jwt_token": user_token})
    else:
        return Response("Invalid Email/Password",status=400)
