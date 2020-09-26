from flask import Flask, render_template, Blueprint, request, Response
import MySQLdb.cursors
from .validate import validate_user_input, generate_hash, generate_salt

def db_write(query, params):
    from app import mysql
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute(query, params)
        mysql.connection.commit()
        cursor.close()

        return True

    except MySQLdb._exceptions.IntegrityError:
        cursor.close()
        return False

user_registration = Blueprint('user_registration', __name__, template_folder='templates')
@user_registration.route('/register', methods = ['GET','POST'])
def register_user():
    from app import mysql
    user_email = request.json["email"]
    user_password = request.json["password"]
    user_confirm_password = request.json["confirm_password"]

    if user_password == user_confirm_password and validate_user_input(
        "authentication", email=user_email, password=user_password
    ):
        password_salt = generate_salt()
        password_hash = generate_hash(user_password, password_salt)
        print("password")
        print(password_hash)
        print(password_salt)

        if db_write(
            """INSERT INTO account (email, password_salt, password_hash) VALUES (%s, %s, %s)""",
            (user_email, password_salt, password_hash),
        ):
            # Registration Successful
            return Response(status=201)
        else:
            # Registration Failed
            return Response(status=409)
    else:
        # Registration Failed
        return Response(status=400)