from models.user import UserModel
from models.blocklist import BlockListModel
from db.db import encrypt, insert_timestamp, decrypt

def authenticate(content, password):
    user = UserModel.find_by_username(content)
    if user:
        if decrypt(content, encrypt(user.username)) and decrypt(password, user.password):
            if (BlockListModel.find_by_user_id(user.id)) is None:
                user.last_login_timestamp = insert_timestamp()
                user.save_to_db()
                return user
    user = UserModel.find_by_email(content)
    if user:
        if decrypt(content, encrypt(user.email)) and decrypt(password, user.password):
            if (BlockListModel.find_by_user_id(user.id)) is None:
                user.last_login_timestamp = insert_timestamp()
                user.save_to_db()
                return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
