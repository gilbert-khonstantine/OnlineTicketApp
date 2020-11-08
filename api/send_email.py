from flask import Flask, render_template
from flask_mail import Mail, Message
import random
import string


def send_2fa(user):
    from app import mail
    
    twoFA = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    msg = Message('2FA', sender = 'danieltechtips2006@gmail.com', recipients = ['danieltechtips2006@gmail.com'])

    msg.html = render_template('email2fa.html', name=user.name, randomTwoFA=twoFA)

    mail.send(msg)
    return twoFA

def send_receipt(user):
    from app import db, Cart, mail
    import re
    cart = Cart.query.filter_by(user_id=user.id).all()

    total = 0
    for item in cart:
        total = total + (float(item.cost) * float(item.quantity))

    msg = Message('Purchase Receipt', sender = 'danieltechtips2006@gmail.com', recipients = ['danieltechtips2006@gmail.com'])
    msg.html = render_template('emailReceipt.html', name=user.name, cart=cart, total=str("%.2f" % round(total,2)))
    mail.send(msg)
    
    return (cart, total)