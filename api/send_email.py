from flask import Flask
from flask_mail import Mail, Message
import random
import string


def send_2fa():
    from app import mail
    
    twoFA = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    msg = Message('2FA', sender = 'danieltechtips2006@gmail.com', recipients = ['danieltechtips2006@gmail.com'])
    msg.body = "Hello, this is your 2FA: " + twoFA
    mail.send(msg)
    return twoFA