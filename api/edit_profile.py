from flask import Flask, Blueprint, request, Response, jsonify
from .verify import check_email


edit_profile = Blueprint('edit_profile', __name__, template_folder='templates')
@edit_profile.route('/edit_profile', methods = ['GET', 'POST'])
def editProfile():
    from app import User, Account, db

    #assuming input fields are not empty
    id = request.json["id"]
    new_name = request.json["name"].strip()
    new_email = request.json["email"].strip()
    new_age = request.json["age"]
    new_address = request.json["address"].strip()

    #assuming id is the same
    user = User.query.get(id)
    user_account = Account.query.get(id)

    #Checking if requested changes are valid
    if check_email(new_email):
        user_account.email = new_email
        email_updated = True
    else:
        print("Unable to change email")
        email_updated = False

    if len(new_name) != 0:
        user.name = new_name
        name_updated = True
    else:
        print("Unable to change name")
        name_updated = False

    if new_age >= 0 and new_age <= 100: #Acceptable age is 0 to 100
        user.age = new_age
        age_updated = True
    else:
        print("Unable to change age")
        age_updated = False
    
    if len(new_address) != 0 and new_address != user.address:
        user.address = new_address
        address_updated = True
    else:
        print("Unable to change address")
        address_updated = False

    try:
        db.session.commit()
    except:
        return "Unable to commit into database"


    return jsonify({'name_updated': name_updated, 'email_updated': email_updated, 'age_updated': age_updated, 'address_updated': address_updated})