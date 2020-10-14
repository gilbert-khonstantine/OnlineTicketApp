from flask import Flask
from flask_mail import Mail, Message
import random
import string
from app import mail


def send_2fa():
    twoFA = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    msg = Message('2FA', sender = 'danieltechtips2006@gmail.com', recipients = ['novaiscrap@gmail.com'])
    msg.body = "Hello, this is your 2FA: " + twoFA
    mail.send(msg)
    return twoFA