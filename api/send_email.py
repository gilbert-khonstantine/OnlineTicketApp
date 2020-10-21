from flask import Flask, render_template
from flask_mail import Mail, Message
import random
import string


def send_2fa(user):
    from app import mail
    
    twoFA = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    msg = Message('2FA', sender = 'danieltechtips2006@gmail.com', recipients = ['danieltechtips2006@gmail.com'])
    #msg.body = "Hello, this is your 2FA: " + twoFA
    #msg.html = '<h1 style="text-align:center;">Hi, this is your 2FA</h1>'

    #msg.html = '<!DOCTYPE html>\
    #            <html>\
    #            <head>\
    #                <h1 style="text-align:center;">Hello {username}</h1>\
    #            </head>\
    #            \
    #            <body>\
    #                <p style="text-align:center;">Thank you for being a loyal customer.<br>\
    #                Here is your 2FA code to continue your tokens purchase:<br>\
    #                <br><h2 style="text-align:center;">{twoFA}</h2>\
    #                </p>\
    #            </body>\
    #            </html>'.format(username=user.name, twoFA=twoFA)

    msg.html = render_template('email2fa.html', name=user.name, randomTwoFA=twoFA)

    mail.send(msg)
    return twoFA