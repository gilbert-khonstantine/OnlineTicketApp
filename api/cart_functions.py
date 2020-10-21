from sqlalchemy import update, engine
from flask import Flask, render_template, url_for, request, redirect, jsonify


def getCart(id):
    from app import db, Cart
    cart = Cart.query.filter_by(user_id=id).all()
    length = len(cart)
    id = []
    product = []
    quantity = []
    cost = []
    for i in range(length):
        id.append(cart[i].id)
        product.append(cart[i].product)
        quantity.append(cart[i].quantity)
        cost.append(cart[i].cost)
    return length, product, quantity, cost


def UpdateCart(id, product, qty):
    from app import db, Cart
    if qty != 0:
        update = Cart.query.filter_by(uid=id).filter_by(product=product).update(dict(amount=qty))
    else:
        delete = Cart.query.filter_by(uid=id).filter_by(product=product).delete()
    db.session.commit()