from models.user import UserModel
from models.blocklist import BlockListModel
from db.db import encrypt, insert_timestamp, decrypt

def auth_by_username(content: str, password: str):
    user = UserModel.find_by_username(content)
    if user:
        if decrypt(password, user.password):
            if (BlockListModel.find_by_user_id(user.id)) is None:
                user.last_login_timestamp = insert_timestamp()
                user.save_to_db()
                return user
    auth_by_email(content, password)

def auth_by_email(content: str, password: str):
    user = UserModel.find_by_email(content)
    if user:
        if decrypt(password, user.password):
            if (BlockListModel.find_by_user_id(user.id)) is None:
                user.last_login_timestamp = insert_timestamp()
                user.save_to_db()
                return user
    return {"message": "invalid credentials"}, 401
