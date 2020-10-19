from flask import Flask, render_template, Blueprint, request, Response, jsonify, make_response

def get_results(search_word):
    from app import db, Product
    from sqlalchemy import or_

    results = Product.query.filter(
        or_(
            Product.title.contains(search_word),
            Product.tag.like(search_word)
        )
    ).all()

    length = len(results)
    print(length)
    id=[]
    title=[]
    price=[]
    duration=[]
    image=[]
    for i in range(length):
        id.append(results[i].id)
        title.append(results[i].title)
        price.append(results[i].price)
        duration.append(results[i].duration)
        image.append(results[i].image_link)
    return (id,title,price,duration,image)
