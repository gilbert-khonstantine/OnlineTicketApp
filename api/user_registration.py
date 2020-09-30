from flask import Flask, render_template, Blueprint, request, Response
from .validate import validate_user_registration
from .utils import generate_hash, generate_salt

user_registration = Blueprint('user_registration', __name__, template_folder='templates')
@user_registration.route('/register', methods = ['GET','POST'])
def register_user():
    from app import db, Account
    if request.method == "POST":
        user_email = request.json["email"]
        user_password = request.json["password"]
        user_confirm_password = request.json["confirm_password"]

        if user_password == user_confirm_password and validate_user_registration(
            "authentication", email=user_email, password=user_password
        ):
            password_salt = generate_salt()
            password_hash = generate_hash(user_password, password_salt)
            new_user = Account(email=user_email, password_salt = password_salt, password_hash = password_hash)
            try:
                db.session.add(new_user)
                db.session.commit()
                return Response("Account created", status=201, mimetype='application/json')
            except:
                return Response("Email is already exist",status=409)
        else: 
            return Response("Invalid Input",status=400)