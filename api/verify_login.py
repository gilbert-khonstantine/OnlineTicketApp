from flask_sqlalchemy import SQLAlchemy
import re

def contains_caps(text):
    return len(re.findall('([A-Z]+)', text)) != 0

def contains_lowercase(text):
    return len(re.findall('([a-z]+)', text)) != 0

def contains_specialCharacters(text):
    special_characters = re.compile('[@_!#$%^&*()<>?/\|}{~:-]') 
    return special_characters.search(text) != None

def contains_number(text):
     return any(char.isdigit() for char in text)

def check_password(password):
    if contains_specialCharacters(password) and contains_caps(password) and contains_lowercase(password) and contains_number(password) and len(password)>8:
        return True
    return False

def check_email(new_email):
    from app import db, User, UserInfo

    #Assume email is passed in as proper email format (something@something.com)
    #Check that email is not empty
    if len(new_email) == 0:
        return False

    #example@example.com || example@example.sg 
    regex = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}$'
    #example@example.edu.sg || example@example.edu.sg
    regexExtra = '^[a-zA-Z0-9]+[\._]?[a-zA-Z0-9]+[@]\w+[.]\w{2,3}[.]\w{2,3}$'
    #NTU email
    regexNTU = '^[a-zA-Z0-9]+@e\.ntu\.edu\.sg$'

    check = re.search(regex, new_email)
    checkExtra = re.search(regexExtra, new_email)
    checkNTU = re.search(regexNTU, new_email)

    if not check and not checkExtra and not checkNTU:
        return False
    
    #Query to check if requested email change is already in use
    existing_email = User.query.filter_by(email=new_email).first()

    if existing_email:
        return False
    
    return True