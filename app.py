from flask import Flask, render_template, Blueprint
from api.user_login import user_login
from api.user_registration import user_registration
from flask_jwt import JWT, jwt_required, current_identity
from api.utils import JWT_SECRET_KEY
from api.validate import validate_user_login, jwt_identity
from flask_sqlalchemy import SQLAlchemy
from api.user_login import user_login

app = Flask(__name__)
app.config['SECRET_KEY'] = JWT_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_account.db'
db = SQLAlchemy(app)
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_salt = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return {"id":self.id,"email":self.email,"password_salt":self.password_salt,"password_hash":self.password_hash}
db.create_all()
jwt = JWT(app, validate_user_login, jwt_identity)

app.register_blueprint(user_login, url_prefix='/api')
app.register_blueprint(user_registration, url_prefix='/api')
# two decorators, same function
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html', the_title='Login')

@app.route('/register')
def register():
    return render_template('register.html', the_title='Register')

@app.route('/home')
def home():
    return render_template('base.html', the_title='Tiger in Myth and Legend')

@app.route('/test_jwt')
@jwt_required()
def jwt():
    return "jwt"

if __name__ == '__main__':
    app.run(debug=True)
