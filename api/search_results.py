from flask import Flask, render_template, Blueprint, request, Response, jsonify, make_response
from autocorrect import Speller

def get_results(search_word):
    from app import db, Product
    from sqlalchemy import or_

    results = Product.query.filter(
        or_(
            Product.title.contains(search_word),
            Product.tag.contains(search_word),
            Product.subtag.contains(search_word)
        )
    ).all()

    length = len(results)
    id=[]
    title=[]
    price=[]
    image=[]
    for i in range(length):
        id.append(results[i].id)
        title.append(results[i].title)
        price.append(results[i].price)
        image.append(results[i].image_link)
    return (id,title,price,image,length)

def get_product(product_id):
    from app import db, Product
    results = Product.query.get(product_id)
    return(results.title,results.price,results.duration,results.description,results.image_link)

def check_spelling(search_word):
    spell = Speller(lang='en')
    search = search_word.split()
    corrected = []

    for word in search:
        corrected.append(spell(word))

    corrected = ' '.join(corrected)

    return corrected
