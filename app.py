import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from datetime import timedelta
from security import authenticate, identity
from resources.user import (User, UserRegister,
                            UserList, UserGetItem, UserCart)
from resources.item import Item, ItemList, ItemToStore
from resources.store import Store, StoreList
from resources.payment import Payment, PaymentList
from resources.blocklist import BlockList, BlockListShow
from db.db import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db/data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_AUTH_URL_RULE'] = '/login'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=1)

app.secret_key = os.urandom(16).hex()
api = Api(app)
db.init_app(app)
jwt = JWT(app, authenticate, identity)
@app.before_first_request
def create_tables():
    db.create_all()


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

api.add_resource(Payment, '/payment')
api.add_resource(PaymentList, '/payments')

api.add_resource(BlockList, '/block_user')
api.add_resource(BlockListShow, '/blocklist')

if __name__ == '__main__':
    from db.db import db
    db.init_app(app)

    app.run(port=5000, debug=True)
