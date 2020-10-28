from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from flask_cors import CORS
from sqlalchemy import and_, func
from api import verify_email
from api import verify_profile
from api import send_email
from api import search_results
from api import cart_functions
from api import history_functions
from api import add_to_history
from random import shuffle
import re

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

#Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticketapp.db'
db = SQLAlchemy(app)

#Auto-email config
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'danieltechtips2006@gmail.com'
app.config['MAIL_PASSWORD'] = 'safetyIsNumber1Priority'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail= Mail(app)

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

# Purchase history
class UserHist(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    product = db.Column(db.String(255), nullable=True)
    quantity = db.Column(db.Integer, nullable = True)
    cost = db.Column(db.Integer, nullable=True)
    datecreated = db.Column(db.DateTime, nullable=True, server_default=func.now())
    def __repr__(self):
        return '<UserHist %r>' % self.id

# Favourite database
class UserFav(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(255), default='0'*3)
    subtags = db.Column(db.String(255), default='0'*20)

    def __repr__(self):
        return '<UserFav %r>' % self.id

''' Unused class
class Payment(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True)
    payment_items = db.relationship('Item', backref='payment', lazy='dynamic')
    shipping = db.Column(db.String(100), nullable=False)
    payment_method = db.Column(db.String(100), nullable=False)
        
    def __repr__(self):
        return '<Payment %r>' % self.id

Unused class
class Item(db.Model):
    __tablename__ = 'item'
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
        
    def __repr__(self):
        return '<Item %r>' % self.id
''' 
# Product info
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(1000), nullable=False)
    price = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    tag = db.Column(db.String(255), nullable=False)
    subtag = db.Column(db.String(255), nullable=False)
    image_link = db.Column(db.String(1000), nullable=False)
    view_count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id

# All user's cart info
class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    product = db.Column(db.String(1000), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return '<Cart %r>' % self.id

db.create_all()

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
            return render_template('login.html', text=text)
    else:
        text = "You're already logged in dude!"
        return redirect('/home')

@app.route('/logout')
def logout():
    global userID
    global text
    if userID!=0:
        userID = 0
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
            text=""
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
            word=request.form['search']
            return redirect('/results/'+word)
        else:
            top12_product = Product.query.order_by(Product.view_count.desc()).limit(12).all() # sorting based on view count and select top 12 products
            for row in range(len(top12_product)):
                top12_product[row].price = re.sub('[S$]','',top12_product[row].price)
            print(top12_product[0].view_count)
            print(top12_product[0].title)
            print(top12_product[2].title)
            print(top12_product[2].view_count)
            print(top12_product)

            # check for user's chosen tags
            user = User.query.get(userID)
            user_fav = UserFav.query.get(userID)
            print(user, user_fav)

            # get tags/subtags values
            tag_val = user_fav.tags
            subtag_val = user_fav.subtags
            tag_names = ['Attractions', 'Movies', 'Museums']
            subtag_names = (['Nature', 'Theme park', 'Others', 'Action', 'Adventure', 'Animation', 'Comedy',
                            'Concert', 'Drama', 'Family', 'Fantasy', 'Horror', 'Musical', 'Mystery',
                            'Romance', 'Sci-Fiction', 'Suspense', 'Thriller', 'Art/Design', 'History'])
            tag_list = []
            subtag_list = []

            # if 1, tag/subtag valid for favourite
            for i in range(len(tag_names)):
                if tag_val[i] == '1':
                    tag_list.append(tag_names[i])

            for i in range(len(subtag_names)):
                if subtag_val[i] == '1':
                    subtag_list.append(subtag_names[i])

            print(tag_val, tag_list)
            print(subtag_val, subtag_list)
                    
            # get products matching chosen tags
            #temp = Product.query.filter(Product.tag.in_(tag_list)).filter(Product.subtag.in_(subtag_list)).all()
            temp = Product.query.filter(Product.tag.in_(tag_list)).all()

            # get products containing subtags as substring
            all_fav = [x for x in temp for y in subtag_list if y in x.subtag]
            all_fav = list(set(all_fav))
            print(len(all_fav))
            shuffle(all_fav)

            if len(all_fav) > 12:
                fav = all_fav[0:12]
            else:
                fav = all_fav
            for row in range(len(fav)):
                fav[row].price = re.sub('[S$]','',fav[row].price)

            print(len(all_fav), *[p for p in fav], sep='\n')
            return render_template('home.html', user=user, text=text, products = top12_product, fav=fav, numloop=len(all_fav))
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/update_view_count', methods=['POST'])
def update_view_count():
    if userID!=0:
        user = User.query.get(userID)
        if request.method=='POST':
            pid = request.json['product_id']
            print("pid: ",pid)
            viewed_product = Product.query.filter_by(id=str(pid)).first()
            viewed_product.view_count = viewed_product.view_count + 1
            db.session.commit()
            return {"message":"ok"}
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
            new_details = (new_name,new_email,new_password,new_age,new_address,new_mobile)
            user_email = user.email
            fail = False
            fail = verify_profile.check_account(fail,new_details,user_email)
            if not fail:
                try:
                    user.name = new_name
                    user.email = new_email
                    user.password = new_password
                    user_info.age = new_age
                    user_info.address = new_address
                    user_info.mobile = new_mobile                    
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

        tag_val = ''
        subtag_names = (['nature', 'theme_park', 'others', 'action', 'adventure', 'animation', 'comedy',
                        'concert', 'drama', 'family', 'fantasy', 'horror', 'musical', 'mystery',
                        'romance', 'sci_fiction', 'suspense', 'thriller', 'art_design', 'history'])
        subtag_val = ''
        values = [0]*len(subtag_names)
             
        if request.method == 'POST':  
            for i in range(len(subtag_names)):
                if request.form.get(subtag_names[i]):
                    subtag_val += '1'
                else:
                    subtag_val += '0'
                
            try:
                if '1' in subtag_val[0:3]: tag_val += '1'
                else: tag_val += '0'
                if '1' in subtag_val[3:18]: tag_val += '1'
                else: tag_val += '0'
                if '1' in subtag_val[18:]: tag_val += '1'
                else: tag_val += '0'

                user_fav.tags = tag_val
                user_fav.subtags = subtag_val
                #print(user_fav.tags, user_fav.subtags, sep='\n')
                db.session.commit()

                for i in range(len(subtag_names)):
                    if user_fav.subtags[i] == '1':
                        values[i] = 'checked'
                    else:
                        values[i] = 'unchecked'
                        
                text = "Favourites updated!"
                return render_template('favourites.html', user=user, user_fav=user_fav,values=values, text=text)
            
            except:
                text = "Update failed!"
                return render_template('favourites.html', user=user, user_fav=user_fav,values=values, text=text)
        else:
            for i in range(len(subtag_names)):
                    if user_fav.subtags[i] == '1':
                        values[i] = 'checked'
                    else:
                        values[i] = 'unchecked'
                    
            text = ""
            return render_template('favourites.html', user=user, user_fav=user_fav,values=values, text=text)
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/history', methods=['POST','GET'])
def history():
    global text
    if userID!=0:
        user = User.query.get(userID)
        data = history_functions.getPurchaseHist(userID)
        text = "Buy more products"
        print(data)
        return render_template('history.html', user=user,len=data[0],product=data[1],quantity=data[2],cost=data[3], datetime=data[4])
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

@app.route('/bank', methods=['POST','GET'])
def bank():
    global total
    global text
    global twofa
    if userID!=0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)
        if request.method == 'POST':
            card_num = request.form['card_num']
            twoFA =  request.form['twofa']
            if len(card_num)==16 and card_num[0]=='4' and int(card_num):
                if twoFA == twofa:
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
                    return render_template('bank.html', user=user, text=text)
            else:
                text="Wrong card details, 16 digits, card starts with 4"
                return render_template('bank.html', user=user, text=text)
        else:
            twofa = send_email.send_2fa(user)
            text=''
            return render_template('bank.html', user=user, text=text)
    else:
        text = "Please login to an account!"
        return redirect('/login')

#in progress
@app.route('/results/<word>', methods=['POST','GET'])
def results(word):
    global text
    search = word
    if userID!=0:

        is_add_text = False
        add_text = ''
        result = search_results.get_results(search)
        num_results = result[4]

        # if initial search returns no entry, apply spelling check
        # display results for corrected spelling if it return entries
        if num_results == 0:
            corrected = search_results.check_spelling(search)
            new_result = search_results.get_results(corrected)
            num_new_results = new_result[4]

            if num_new_results != num_results:
                is_add_text = True
                add_text = 'Displaying results for ' + corrected + ' instead'
                result = new_result
        
        return render_template('results.html',
                                word=search,
                                text="Here are the results",
                                is_add_text = is_add_text,
                                add_text = add_text,
                                pid=result[0],
                                title=result[1],
                                price = [re.sub('[S$]','', p) for p in result[2]],
                                image=result[3])
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/details/<id>', methods=['POST','GET'])
def details(id):
    global text
    product_id = id
    if userID!=0:
        result = search_results.get_product(product_id)
        return render_template('details.html',
                                word=product_id,
                                text="Here are the details",
                                title=result[0],
                                price = re.sub('[S$]','', result[1]),
                                duration=result[2],
                                description=result[3],
                                image=result[4])
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route("/add_to_cart", methods=['POST'])
def add_to_cart():
    title = request.json['product_title']
    cost = request.json['product_price']
    have = Cart.query.filter_by(product = title, cost = cost, user_id = userID).all()
    if have == []:
        newItem = Cart(user_id=userID,product=title,quantity=1,cost=cost)
        db.session.add(newItem)
    else:
        have[-1].quantity = have[-1].quantity+1
    db.session.commit()
    return {"msg":"success"}

@app.route('/cart', methods=['POST','GET'])
def cart():
    global text
    if userID!=0:
        user = User.query.get(userID)
        data = cart_functions.getCart(userID)
        return render_template('cart.html', user=user, len=data[0],product=data[1],quantity=data[2],cost=data[3])
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/updatecart', methods=['POST','GET'])
def updatecart():
    name = request.json['product_title']
    qty = request.json['product_qty']
    price = request.json['product_price']
    action = request.json['action']
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id = db.Column(db.Integer, nullable=False)
    # product = db.Column(db.String(1000), nullable=False)
    # quantity = db.Column(db.Integer, nullable=False)
    # cost = db.Column(db.Integer, nullable=False)
    if action == "add":
        # selected_item = Cart.query.filter_by(product=name,quantity=qty,cost=price).all()
        selected_item = Cart.query.filter_by(product=name,quantity=int(qty)-1).all()[-1]
        selected_item.quantity = selected_item.quantity + 1
    elif action == "subtract":
        selected_item = Cart.query.filter_by(product=name,quantity=int(qty)+1).all()[-1]
        selected_item.quantity = selected_item.quantity - 1
        if selected_item.quantity == 0:
            Cart.query.filter_by(product=name,quantity=int(qty)).delete()
    elif action == "delete":
        Cart.query.filter_by(product=name,quantity=int(qty)).delete()
    db.session.commit()
    return {"msg": "success"}

@app.route('/payment', methods=['POST','GET'])
def payment():
    global text
    if userID!=0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)
        results = cart_functions.getCart(userID)
        total = 0
        price = list.copy(results[3])
        quan = list.copy(results[2])
        print(price)
        for i in range(results[0]):
            total = total + float(price[i]) * float(quan[i])
        total = "S$" + str(total)
        text=""
        return render_template('payment.html',
                                user = user,
                                tokens = user_info.token,
                                product = results[1],
                                quantity = results[2],
                                cost = results[3],
                                total = total)
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/deduct', methods=['POST','GET'])
def deduct():
    global text
    if userID!=0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)
        total = request.json['total_price']
        price=total
        print(price)
        if user_info.token - float(price) < 0:
            text = "Insufficient tokens, please top-up. Your total cart price is: S$" + total
            return {'msg':'failed'}
        else:
            balance = user_info.token - float(price)
            user_info.token = float(balance)
            db.session.commit()
            text="Tokens deducted"
            return {'msg':'success'}
    else:
        text = "Please login to an account!"
        return redirect('/login')

@app.route('/receipt')
def receipt():
    global text
    if userID!=0:
        user = User.query.get(userID)
        user_info = UserInfo.query.get(userID)

        if add_to_history.addHistory(user):
            send_email.send_receipt(user)
            if add_to_history.deleteCart(user):
                text="success"
            else:
                text="delete not ok"
        else:
            text=text+"adding not ok"
        return render_template('receipt.html', user=user, text=text)
    else:
        text = "Please login to an account!"
        return redirect('/login')
    
if __name__ == "__main__":
    #Create variable to store logged in userID
    userID = 0
    #Create variable to send text to each html page
    text = ""
    #Create variable to store twofa to compare with user input
    twofa = ""
    app.run(debug=True)
