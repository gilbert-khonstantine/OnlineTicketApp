from .utils import generate_hash, generate_jwt_token, JWT_SECRET_KEY
import datetime

def jwt_identity(payload):
    print(payload)
    user_id = payload['id']
    return user_id

def validate_user_login(email, password):
    from app import Account
    current_user = Account.query.filter_by(email=str(email)).first_or_404()
    current_user = {"id":current_user.id,"email":current_user.email,"password_salt":current_user.password_salt,"password_hash":current_user.password_hash}
    print(current_user)
    if current_user['id'] >= 0:
        saved_password_hash = current_user["password_hash"]
        saved_password_salt = current_user["password_salt"]
        password_hash = generate_hash(password, saved_password_salt)
        print(password_hash)

        if password_hash == saved_password_hash:
            user_id = current_user["id"]
            jwt_token = generate_jwt_token({"id": user_id,'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=900000), 'iat': datetime.datetime.utcnow(),'nbf': datetime.datetime.utcnow()})
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

