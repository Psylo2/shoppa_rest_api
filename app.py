import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from datetime import timedelta
from blacklist import BLACKLIST
from resources.user import (User, UserRegister,
                            UserList, UserGetItem, UserCart,
                            UserLogin, TokenRefresh,
                            UserLogout)
from resources.item import Item, ItemList, ItemToStore
from resources.store import Store, StoreList
from resources.payment import Payment, PaymentList
from resources.blocklist import BlockList, BlockListShow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db/data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=10)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(minutes=1)
# app.config['JWT_TOKEN_LOCATION'] = 'cookies'
# app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# app.config['SESSION_COOKIE_SECURE '] = True
app.config['JWT_BLACKLIST_ENABLED'] = True  # enable blacklist feature
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = [
    "access",
    "refresh",
]
app.config['JWT_SECRET_KEY'] = os.urandom(16).hex()
app.secret_key = os.urandom(16).hex()
api = Api(app)
jwt = JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api.add_resource(Store, '/store')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item')
api.add_resource(ItemList, '/items')
api.add_resource(ItemToStore, '/item_to_store')

api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserGetItem, '/user_get_item')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')
api.add_resource(UserCart, '/cart')
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")

api.add_resource(Payment, '/payment')
api.add_resource(PaymentList, '/payments')

api.add_resource(BlockList, '/block_user')
api.add_resource(BlockListShow, '/blocklist')

if __name__ == '__main__':
    from db.db import db
    db.init_app(app)

    app.run(port=5000, debug=True)
