import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import User, UserRegister, UserList, UserGetItem
from resources.item import Item, ItemList, ItemToStore
from resources.store import Store, StoreList

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db/data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_password'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(Item, '/item/<string:item_name>')
api.add_resource(ItemList, '/items')
api.add_resource(ItemToStore, '/item_to_store')

api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserGetItem, '/user_get_item')
api.add_resource(UserRegister, '/register')
api.add_resource(UserList, '/users')

if __name__ == '__main__':
    from db.db import db
    db.init_app(app)

    app.run(port=5000, debug=True)
