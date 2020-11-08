from datetime import datetime

def addHistory(user):
    from app import db, UserHist, Cart
    
    cart = Cart.query.filter_by(user_id=user.id).all()

    try:
        for item in cart:
            itemToAdd = UserHist(user_id=user.id, product=item.product, quantity=item.quantity, cost=item.cost)
            db.session.add(itemToAdd)

        db.session.commit()
        return True
    except:
        return False

def deleteCart(user):
    from app import db, UserHist, Cart

    cart = Cart.query.filter_by(user_id=user.id).all()

    try:
        for item in cart:
            db.session.delete(item)
            
        db.session.commit()
        return True
    except:
        return False