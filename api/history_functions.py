from flask import Flask, render_template, url_for, request, redirect, jsonify

def getPurchaseHist(id):
    from app import db, UserHist
    purhist = UserHist.query.filter_by(user_id=id).all()
    length = len(purhist)
    id = []
    product = []
    quantity = []
    cost = []
    datetime = []
    for i in range(length):
        id.append(purhist[i].id)
        product.append(purhist[i].product)
        quantity.append(purhist[i].quantity)
        cost.append(purhist[i].cost)
        datetime.append(purhist[i].datecreated)
    return length, product, quantity, cost, datetime
