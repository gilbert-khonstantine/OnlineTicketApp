from flask import Flask, Blueprint, request, Response, jsonify

get_profile = Blueprint('get_profile', __name__, template_folder='templates')
@get_profile.route('/get_profile', methods = ['GET', 'POST'])
def getProfile():
    from app import User

    user_id = request.json["id"]
    user = User.query.get(user_id)
    return jsonify({"name":user.name, "email":"hello@user.com", "age":user.age, "address":user.address})