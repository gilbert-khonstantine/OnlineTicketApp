from flask import Flask, render_template, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from api.user_login import user_login
from api.get_profile import get_profile
from api.edit_profile import edit_profile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Account(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_salt = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Account %r>' % self.id

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    
    def __repr__(self):
        return '<User %r>' % self.ids

app.register_blueprint(get_profile, url_prefix='/api')
app.register_blueprint(edit_profile, url_prefix='/api')
app.register_blueprint(user_login, url_prefix='/api')
# two decorators, same function
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html', the_title='Tiger Home Page')

@app.route('/symbol.html')
def symbol():
    return render_template('symbol.html', the_title='Tiger As Symbol')

@app.route('/myth.html')
def myth():
    return render_template('myth.html', the_title='Tiger in Myth and Legend')

def main():
    user = User(name="user", age=17, address="user street", account_id=1)
    db.session.add(user)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
