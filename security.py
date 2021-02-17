from models.user import UserModel
import bcrypt

def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user:
        if decrypt(username, user.username) and decrypt(password, user.password):
            return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)


def decrypt(x, y):
    return bcrypt.checkpw(x.encode("UTF-8"), y)

