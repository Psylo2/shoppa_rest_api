import os
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister, UserList, User
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///db/data.db')
app.config['PROPAGATE_EXCEPTIONS'] = True # To allow flask propagating exception even if debug is set to false on app
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'pablo'
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:item_name>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:use_id>')
api.add_resource(ItemList, '/items')
api.add_resource(UserList, '/users')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)  # important to mention debug=True