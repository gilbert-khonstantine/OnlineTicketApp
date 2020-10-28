''' Unused

from flask import Flask, render_template, Blueprint, request, Response, jsonify, make_response

def validate_payment(balance):
    if balance >= 0:
        return True

    else:
        return False

# following the mockup UI template
def payment(token):
    from app import Payment, db

    user_token = token
    print(user_token)
    payment = Payment.query.get(1) # should eventually link it to user's ID
    
    itemlist = [[item.item, item.cost] for item in payment.payment_items]
    subtotal = sum([item.cost for item in payment.payment_items])
    discount = 10
    total = subtotal - discount
    shipping = payment.shipping
    payment_method = payment.payment_method
    
    print(itemlist, total)

    if validate_payment(user_token-total):
        return (True, itemlist, subtotal, discount, total, shipping, payment_method) # returns a tuple
    
    else:
        return (False, 0)