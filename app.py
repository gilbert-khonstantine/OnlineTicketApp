
from flask import Flask, render_template, url_for, request, redirect, jsonify
#from makeDB import User, UserFav, UserInfo, UserHist, productlist
from flask_sqlalchemy import SQLAlchemy
from api import make_payment
from flask import Flask, render_template, Blueprint
from api.user_login import user_login
from api.user_registration import user_registration
from flask_jwt import JWT, jwt_required, current_identity
from api.utils import JWT_SECRET_KEY
from api.validate import validate_user_login, jwt_identity
from flask_sqlalchemy import SQLAlchemy
from api.user_login import user_login

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SECRET_KEY'] = JWT_SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # suppress warning message
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
db = SQLAlchemy(app)

# Login info
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.id

# Other info
class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    mobile = db.Column(db.String(255), nullable=True)
    token = db.Column(db.Integer, default=0)
    def __repr__(self):
        return '<UserInfo %r>' % self.id

# Purchase history (2 primary keys)
class UserHist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    product = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    datecreated = db.Column(db.DateTime, nullable=False)
    def __repr__(self):
        return '<UserHist %r>' % self.id

# Favourite database
class UserFav(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    tag1 = db.Column(db.Boolean, default=0)
    tag2 = db.Column(db.Boolean, default=0)
    tag3 = db.Column(db.Boolean, default=0)
    tag4 = db.Column(db.Boolean, default=0)
    tag5 = db.Column(db.Boolean, default=0)
    tag6 = db.Column(db.Boolean, default=0)
    def __repr__(self):
        return '<UserFav %r>' % self.id

# Payment info
class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    payment_items = db.relationship('Item', backref='payment', lazy='dynamic')
    shipping = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)
        
    def __repr__(self):
        return '<Payment %r>' % self.id

# Item info
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
        
    def __repr__(self):
        return '<Item %r>' % self.id

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_salt = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return {"id":self.id,"email":self.email,"password_salt":self.password_salt,"password_hash":self.password_hash}
db.create_all()
jwt = JWT(app, validate_user_login, jwt_identity)

# clear all existing rows in all tables before running new testcases
def clear_data(session):
    meta = db.metadata
    
    for table in reversed(meta.sorted_tables):
        print('Clear table %s' % table)
        session.execute(table.delete())
        
    session.commit()
    
app.register_blueprint(user_login, url_prefix='/api')
app.register_blueprint(user_registration, url_prefix='/api')

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html', the_title='Login')

@app.route('/register')
def register():
    return render_template('register.html', the_title='Register')

@app.route('/logout')
def logout():
    return render_template('login.html', the_title='Login')

@app.route('/home', methods=['POST','GET'])
def home():
    global text
    global search
    # if userID!=0:
    user = User.query.get(userID)
    if request.method=='POST':
        search = request.form['search']
        return redirect('/results')
    else:
        text=""
        return render_template('home.html', user=user, text=text)
    # else:
    #     text = "Please login to an account!"
    #     return redirect('/login')

#how to check valid email logic
@app.route('/profile', methods=['POST', 'GET'])
def profile():
    global text
    if userID != 0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)
        if request.method == 'POST':
            user.name = request.form['name']
            user.email = request.form['email']
            user.password = request.form['password']
            user_info.age = request.form['age']
            user_info.address = request.form['address']
            user_info.mobile = request.form['mobile']
            try:
                db.session.commit()
                text="Profile updated!"
                return render_template('profile.html', user=user, user_info=user_info, text=text)
            except:
                text="Update failed!"
                return render_template('profile.html', user=user, user_info=user_info, text=text)
        else:
            text=""
            return render_template('profile.html', user=user, user_info=user_info, text=text)
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/favourites', methods=['POST','GET'])
def favourites():
    global text
    if userID!=0:
        user = User.query.get(userID)
        user_fav = UserFav.query.get(userID)
        if request.method == 'POST':
            if request.form.get('pop'): user_fav.tag1 = True
            else: user_fav.tag1 = False
            if request.form.get('rock'): user_fav.tag2 = True
            else: user_fav.tag2 = False
            if request.form.get('indie'): user_fav.tag3 = True
            else: user_fav.tag3 = False
            if request.form.get('blues'): user_fav.tag4 = True
            else: user_fav.tag4 = False
            if request.form.get('zoo'): user_fav.tag5 = True
            else: user_fav.tag5 = False
            if request.form.get('amusement_park'): user_fav.tag6 = True
            else: user_fav.tag6 = False
            try:
                db.session.commit()
                if user_fav.tag1 == True: value1 = 'checked'
                else: value1 = 'unchecked'
                if user_fav.tag2 == True: value2 = 'checked'
                else: value2 = 'unchecked'
                if user_fav.tag3 == True: value3 = 'checked'
                else: value3 = 'unchecked'
                if user_fav.tag4 == True: value4 = 'checked'
                else: value4 = 'unchecked'
                if user_fav.tag5 == True: value5 = 'checked'
                else: value5 = 'unchecked'
                if user_fav.tag6 == True: value6 = 'checked'
                else: value6 = 'unchecked'
                text = "Favourites updated!"
                return render_template('favourites.html', user=user, user_fav=user_fav,value1=value1,value2=value2,value3=value3,value4=value4,value5=value5,value6=value6, text=text)
            except:
                text = "Update failed!"
                return render_template('favourites.html', user=user, user_fav=user_fav,value1=value1,value2=value2,value3=value3,value4=value4,value5=value5,value6=value6, text=text)
        else:
            if user_fav.tag1 == True: value1 = 'checked'
            else: value1 = 'unchecked'
            if user_fav.tag2 == True: value2 = 'checked'
            else: value2 = 'unchecked'
            if user_fav.tag3 == True: value3 = 'checked'
            else: value3 = 'unchecked'
            if user_fav.tag4 == True: value4 = 'checked'
            else: value4 = 'unchecked'
            if user_fav.tag5 == True: value5 = 'checked'
            else: value5 = 'unchecked'
            if user_fav.tag6 == True: value6 = 'checked'
            else: value6 = 'unchecked'
            text=""
            return render_template('favourites.html', user=user, user_fav=user_fav,value1=value1,value2=value2,value3=value3,value4=value4,value5=value5,value6=value6, text=text)
    else:
        text = "Please login to an account!"
        return redirect('/login')

#how to change hist into array and pass to html logic
@app.route('/history', methods=['POST','GET'])
def history():
    global text
    if userID!=0:
        user = User.query.get(userID)
        user_hist = UserHist.query.filter_by(user_id=userID).all()
        data=""
        if user_hist is not None:
            if user_hist is not None:
                for row in user_hist:
                    data = data + str(row.product) + ',' + str(row.amount) + ',' + str(row.cost) + ','
                data = data[:-1]
        return render_template('history.html', user=user, text=text, purHist=data)
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/tokens', methods=['POST','GET'])
def tokens():
    global text
    global total_tokens
    if userID!=0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)
        if request.method=="POST":
            value = request.form['amount']
            current = user_info.token
            total_tokens = int(current) + int(value)
            text=''
            return redirect('/bank')
        else:
            return render_template('tokens.html', user=user, user_info=user_info, text=text)
    else:
        text = "Please login to an account!"
        return redirect('/login')

#how to send 2fa???
@app.route('/bank', methods=['POST','GET'])
def bank():
    global total_tokens
    global text
    if userID!=0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)
        if request.method == 'POST':
            card_num = request.form['card_num']
            twoFA =  request.form['twofa']
            if len(card_num)==16 and card_num[0]=='4' and int(card_num):
                if len(twoFA)==3 and int(twoFA):
                    try:
                        user_info.token=total_tokens
                        db.session.commit()
                        total_tokens=0
                        text="Tokens added!"
                        return redirect('/tokens')
                    except:
                        total_tokens=0
                        text="Transaction failed!"
                        return redirect('/tokens')
                else:
                    text='Wrong 2FA'
                    return render_template('bank.html', user=user)
            else:
                text="Wrong card details"
                return render_template('bank.html', user=user)
        else:
            text=''
            return render_template('bank.html', user=user)
    else:
        text = "Please login to an account!"
        return redirect('/login')

#in progress
@app.route('/results', methods=['POST','GET'])
def results():
    global text
    global search
    if userID!=0:
        user = User.query.get(userID)
        return render_template('results.html')
    else:
        text = "Please login to an account!"
        return redirect('/login')

#how to add and decrease amount of tickets
@app.route('/cart', methods=['POST','GET'])
def cart():
    global text
    user = User.query.get(userID)
    return render_template('cart.html', user=user, userCart=userCart)
    # else:
        # text = "Please login to an account!"
        # return redirect('/login')

# payment webpage
@app.route('/payment', methods=['POST','GET'])
def payment():
    t = make_payment.payment()
    user = User.query.get(userID)

    # alternatively, pass tuple t into the html template, then get each variable from the tuple
    # neater for the return function
    if t[0]:
        return render_template('payment.html',
                               the_title = 'Payment',
                               itemlist = t[1],
                               subtotal = t[2],
                               discount = t[3],
                               total = t[4],
                               shipping = t[5],
                               payment_method = t[6],
                               user = user)
    
    else:
        print('Insufficient tokens, please top up!')
        return redirect('/tokens') 

#add deduct token logic here
@app.route('/deduct')
def deduct():
    global text
    if userID!=0:
        userInfo = User.query.get(userID)
        if enough_tokens == True:
            text = "Tokens deducted! Thank you for your purchase!"
            return redirect('/receipt')
        else:
            text = "Insufficient tokens, please top-up!"
            return redirect('/payment')
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/receipt')
def receipt():
    global text
    global userCart
    if userID!=0:
        user = User.query.get(userID)
        if text != "Tokens deducted! Thank you for your purchase!":
            userCart=[]
            text = ""
        return render_template('receipt.html', user=user, text=text)
    else:
        text = "Please login to an account!"
        return redirect('/login')


# put testcases here
def test():
    clear_data(db.session)

    temp_item1 = Item(
        item = 'Nendoroid',
        cost = 20.06,
        )
    temp_item2 = Item(
        item = 'Nintendo Switch Lite',
        cost = 256.32,
        )
    temp_payment = Payment(
        payment_items = [temp_item1, temp_item2],
        shipping = 'Tracked Postage',
        payment_method = 'PayPal'
        )

    db.session.add_all([temp_item1, temp_item2, temp_payment])
    db.session.commit()
    print(temp_payment.payment_items.count()) # check total items in payment
    print(temp_payment.id, temp_item1.id, temp_item1.payment_id, temp_item2.id, temp_item2.payment_id) # make sure item id are linked to correct payment id
    print('testing...')

    
if __name__ == "__main__":
    test()
    userID = 0
    userCart = ["zoo","help","idk"]
    text = ""
    total_tokens = 0
    search = ""
    app.run(debug=True)
