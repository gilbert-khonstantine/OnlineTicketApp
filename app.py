from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from api import verify_email
from api import make_payment

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketapp.db'
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
    product = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Integer, nullable = True)
    cost = db.Column(db.Integer, nullable=True)
    datecreated = db.Column(db.DateTime, nullable=True)
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

@app.route('/')
@app.route('/login', methods=['POST', 'GET'])
def login():
    global userID
    global text
    if userID==0:
        if request.method == 'POST':
            login_email = request.form['email']
            login_password = request.form['password']
            user_to_login = User.query.filter_by(email=str(login_email)).first()
            if user_to_login != None:
                if user_to_login.password == login_password:
                    userID = str(user_to_login.id)
                    text = ""
                    return redirect('/home')
                else:
                    text = "Wrong password!"
                    return render_template('login.html', text=text)
            else:
                text = "No account registered!"
                return render_template('login.html', text=text)
        else:
            text=""
            return render_template('login.html', text=text)
    else:
        text = "You're already logged in dude!"
        return redirect('/home')

@app.route('/logout')
def logout():
    global userID
    global text
    global userCart
    if userID!=0:
        userID = 0
        userCart =[]
        text = "Logged out successfully!"
        return redirect("/login")
    else:
        text = ""
        return redirect("/login")

@app.route('/register', methods=['POST', 'GET'])
def register():
    global text
    if userID==0:
        if request.method == 'POST':
            new_name = request.form['name']
            new_email = request.form['email']
            new_password = request.form['password']
            if verify_email.check_email(new_email):
                new_user = User(name=new_name, email=new_email, password=new_password)
                try:
                    db.session.add(new_user)
                    db.session.commit()
                    latest_user = User.query.filter_by(email=str(new_email)).first()
                    new_user_info = UserInfo(user_id=latest_user.id)
                    new_user_fav = UserFav(user_id=latest_user.id)
                    new_user_hist = UserHist(user_id=latest_user.id)
                    db.session.add(new_user_info)
                    db.session.add(new_user_fav)
                    db.session.add(new_user_hist)
                    db.session.commit()
                    text = "Account created!"
                    return redirect('/login')
                except:
                    text = "Account creation failed! Unknown error!"
                    return redirect('/login')
            else:
                text = "Invalid email!"
                return render_template('register.html', text=text)
        else:
            return render_template('register.html', text=text)
    else:
        text = "You're already logged in dude!"
        return redirect('/home')

#in progress
@app.route('/home', methods=['POST','GET'])
def home():
    global text
    global search
    if userID!=0:
        user = User.query.get(userID)
        if request.method=='POST':
            search = request.form['search']
            return redirect('/results')
        else:
            text=""
            return render_template('home.html', user=user, text=text)
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/profile', methods=['POST', 'GET'])
def profile():
    global text
    if userID != 0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)
        if request.method == 'POST':
            new_name = request.form['name']
            new_email = request.form['email']
            new_password = request.form['password']
            new_age = request.form['age']
            new_address = request.form['address']
            new_mobile = request.form['mobile']
            text=""
            fail = False
            if len(new_name) != 0:
                user.name = new_name
            else:
                text = text + "Invalid username, new name not saved!\n"
                fail = True
            if user.email == new_email:
                user.email = new_email
            else:
                if verify_email.check_email(new_email):
                    user.email = new_email
                else:
                    text = text + "Invalid email, new email not saved!\n "
                    fail = True
            if new_age!="":
                try:
                    new_age = int(new_age)
                    if new_age >= 0 and new_age <= 100: #Acceptable age is 0 to 100
                        user_info.age = new_age
                    else:
                        text = text + "Invalid age, new age not saved!\n "
                        fail = True
                except:
                    text = text + "Invalid age, new age not saved!\n "
                    fail = True
            if new_mobile!="":
                try:
                    int(new_mobile)
                    user_info.mobile = new_mobile
                except:
                    text = text + "Invalid mobile, new mobile not saved!\n"
                    fail = True
            user.password = new_password
            user_info.address = new_address
            if not fail:
                try:
                    db.session.commit()
                    text="Profile updated!"
                    return render_template('profile.html', user=user, user_info=user_info, text=text)
                except:
                    text="Unknown error!"
                    return render_template('profile.html', user=user, user_info=user_info, text=text)
            else:
                try:
                    db.session.commit()
                    text="Update failed!\n"+text
                    return render_template('profile.html', user=user, user_info=user_info, text=text)
                except:
                    text="Unknown error!"
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

@app.route('/history', methods=['POST','GET'])
def history():
    global text
    if userID!=0:
        user = User.query.get(userID)
        user_hist = UserHist.query.filter_by(user_id=userID).all()
        data=""
        if user_hist is not None:
            for row in user_hist:
                data = data + str(row.product) + ',' + str(row.quantity) + ',' + str(row.cost) + ',' + str(row.datecreated) + ','
            data = data[:-1]
        return render_template('history.html', user=user, text=text, purHist=data)
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/tokens', methods=['POST','GET'])
def tokens():
    global text
    global total
    if userID!=0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)
        if request.method=="POST":
            value = request.form['amount']
            current = user_info.token
            total = int(current) + int(value)
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
    global total
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
                        user_info.token=total
                        db.session.commit()
                        total=0
                        text="Tokens added!"
                        return redirect('/tokens')
                    except:
                        total=0
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

#in progress
@app.route('/cart', methods=['POST','GET'])
def cart():
    global text
    if userID!=0:
        user = User.query.get(userID)
        return render_template('cart.html', user=user, userCart=userCart)
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/payment', methods=['POST','GET'])
def payment():
    global text
    if userID!=0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)
        token = user_info.token
        t = make_payment.payment(token)
        text=""
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
    else:
        text = "Please login to an account!"
        return redirect('/login')

#in progress
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
    
if __name__ == "__main__":
    userID = 0
    userCart = ["zoo","help","idk"]
    text = ""
    total = 0
    search = ""
    app.run(debug=True)