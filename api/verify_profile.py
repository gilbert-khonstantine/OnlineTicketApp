from flask import Flask, render_template, Blueprint, request, Response, jsonify, make_response
from .verify_login import check_email

def check_account(fail,new_details,user_email):
    new_name = new_details[0]
    new_email = new_details[1]
    new_age = new_details[2]
    new_address = new_details[3]
    new_mobile = new_details[4]
    fail = False
    text = ""
    if len(new_name) == 0:
        text = "Invalid username, new name not saved!\n"
        fail = True
    if user_email != new_email:
        if not check_email(new_email):
            text = "Invalid email, new email not saved!\n "
            fail = True
    if new_age!="":
        try:
            new_age = int(new_age)
            if not (new_age >= 0 and new_age <= 100): #Acceptable age is 0 to 100
                text = "Invalid age, new age not saved!\n "
                fail = True
        except:
            text = "Invalid age, new age not saved!\n "
            fail = True
    if new_mobile!="":
        try:
            int(new_mobile)
        except:
            text = "Invalid mobile, new mobile not saved!\n"
            fail = True
    
    return (fail, text)