from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from api.user_login import user_login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_salt = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Account %r>' % self.id

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

if __name__ == '__main__':
    app.run(debug=True)
