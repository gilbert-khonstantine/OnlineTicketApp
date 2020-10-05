from flask_sqlalchemy import SQLAlchemy


def check_email(new_email):
    from app import db, User, Account

    #Assume email is passed in as proper email format (something@something.com)
    #Check that email is empty
    if len(new_email) == 0:
        return False
    
    #Query to check if requested email change is already in use
    existing_email = Account.query.filter_by(email=new_email).first()

    if existing_email:
        return False
    else:
        return True