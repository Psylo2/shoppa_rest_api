import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import User, UserRegister, UserList, UserGetItem, UserCart
from resources.item import Item, ItemList, ItemToStore
from resources.store import Store, StoreList
from db.db import db
from resources.blocklist import BlockList, BlockListShow
from datetime import timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db/data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)
# app.config['JWT_SECRET_KEY'] = 'your_Token_secret_password'
app.secret_key = 'your_App_secret_password'
api = Api(app)

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)


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

api.add_resource(BlockList, '/block_user')
api.add_resource(BlockListShow, '/blocklist')



if __name__ == '__main__':
    db.init_app(app)

    app.run(port=5000, debug=True)
