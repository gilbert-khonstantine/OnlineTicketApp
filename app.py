from flask import Flask, render_template, url_for, request, redirect, jsonify
#from makeDB import User, UserFav, UserInfo, UserHist, productlist
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True
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

# List of products
class ProductList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product = db.Column(db.String(255), nullable=False)
    tag = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return '<productlist %r>' % self.id

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

#how to check valid email logic
@app.route('/register', methods=['POST', 'GET'])
def register():
    global text
    if userID==0:
        if request.method == 'POST':
            new_name = request.form['name']
            new_email = request.form['email']
            new_password = request.form['password']
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
                text = "Account creation failed!"
                return redirect('/login')
        else:
            return render_template('register.html', text=text)
    else:
        text = "You're already logged in dude!"
        return redirect('/home')

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

#how to add and decrease amount of tickets
@app.route('/cart', methods=['POST','GET'])
def cart():
    global text
    if userID!=0:
        user = User.query.get(userID)
        return render_template('cart.html', user=user, userCart=userCart)
    else:
        text = "Please login to an account!"
        return redirect('/login')

#how tocalculate total price and pass to html logic
@app.route('/payment', methods=['POST','GET'])
def payment():
    global text
    if userID!=0:
        user = User.query.get(userID)
        text=""
        return render_template('payment.html', user=user, userCart=userCart)
    else:
        text = "Please login to an account!"
        return redirect('/login')

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
    
if __name__ == "__main__":
    userID = 0
    userCart = ["zoo","help","idk"]
    text = ""
    total = 0
    search = ""
    app.run(debug=True)