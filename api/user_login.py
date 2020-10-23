''' Unused

from flask import Flask, render_template, Blueprint, request
import MySQLdb.cursors

user_login = Blueprint('user_login', __name__, template_folder='templates')
@user_login.route('/login')
def login():
    from app import mysql
    if (request.method == "GET"):
        print("GET method")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM ACCOUNT')
    # Fetch one record and return result
    account = cursor.fetchone()
    print(account)
    return account
login.method = ['GET','POST']