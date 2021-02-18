from models.user import UserModel
import bcrypt
from db.db import encrypt, insert_timestamp

def authenticate(content, password):
    user = UserModel.find_by_username(content)
    if user:
        if decrypt(content, encrypt(user.username)) and decrypt(password, user.password):
            user.last_login_timestamp = insert_timestamp()
            user.save_to_db()
            return user
    user = UserModel.find_by_email(content)
    if user:
        if decrypt(content, encrypt(user.email)) and decrypt(password, user.password):
            user.last_login_timestamp = insert_timestamp()
            user.save_to_db()
            return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)


def decrypt(x, y):
    return bcrypt.checkpw(x.encode("UTF-8"), y)

