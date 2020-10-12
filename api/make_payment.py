from flask import Flask, render_template, Blueprint, request, Response, jsonify, make_response
import MySQLdb.cursors
from .validate import validate_payment

#make_payment = Blueprint('make_payment', __name__, template_folder='templates')
#@make_payment.route('/payment', methods = ['GET', 'POST'])


# following the mockup UI template
def payment():
    from app import Payment, db

    token = 600 # should be an attribute under UserInfo/Profile class
    payment = Payment.query.get(1) # should eventually link it to user's ID
    
    itemlist = [[item.item, item.cost] for item in payment.payment_items]
    subtotal = sum([item.cost for item in payment.payment_items])
    discount = 10
    total = subtotal - discount
    shipping = payment.shipping
    payment_method = payment.payment_method
    
    print(itemlist, total)

    if validate_payment(token-total):
        return (True, itemlist, subtotal,
                discount, total, shipping, payment_method) # returns a tuple
    
    else:
        return False
        



