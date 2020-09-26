from .utils import generate_hash, generate_jwt_token, JWT_SECRET_KEY
import datetime

def jwt_identity(payload):
    print(payload)
    user_id = payload['id']
    return user_id

def validate_user_login(email, password):
    def db_read(query, params=None):
        from app import mysql
        cursor = mysql.connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        entries = cursor.fetchall()
        cursor.close()

        content = []

        for entry in entries:
            content.append(entry)

        return content

    current_user = db_read("""SELECT * FROM account WHERE email = %s""", (email,))

    if len(current_user) == 1:
        print(current_user[0])
        saved_password_hash = current_user[0][3]
        saved_password_salt = current_user[0][2]
        print(saved_password_hash)
        print(saved_password_salt)
        password_hash = generate_hash(password, saved_password_salt)

        if password_hash == saved_password_hash:
            user_id = current_user[0][0]
            jwt_token = generate_jwt_token({"id": user_id,'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=9000), 'iat': datetime.datetime.utcnow(),'nbf': datetime.datetime.utcnow()})
            return jwt_token
        else:
            return False

    else:
        return False

def validate_user_registration(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False

