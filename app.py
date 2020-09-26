from flask import Flask, render_template, Blueprint
from flask_mysqldb import MySQL
from api.user_login import user_login
from api.user_registration import user_registration
from flask_jwt import JWT, jwt_required, current_identity
from api.utils import JWT_SECRET_KEY
from api.validate import validate_user_login, jwt_identity

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1808'
app.config['MYSQL_DB'] = 'ticketDB'
app.config['SECRET_KEY'] = JWT_SECRET_KEY

mysql = MySQL(app)

jwt = JWT(app, validate_user_login, jwt_identity)

app.register_blueprint(user_login, url_prefix='/api')
app.register_blueprint(user_registration, url_prefix='/api')
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

@app.route('/test_jwt')
@jwt_required()
def jwt():
    return "jwt"

if __name__ == '__main__':
    app.run(debug=True)
