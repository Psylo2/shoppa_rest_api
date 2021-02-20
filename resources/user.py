from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel
from models.item import ItemModel
from db.db import insert_timestamp
from models.blocklist import BlockListModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="this field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="this field cannot be blank.")
    parser.add_argument('email',
                        type=str,
                        required=False,
                        help="this field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "Username already Taken!"}, 400
        if UserModel.find_by_email(data['email']):
            return {"message": "Email already Taken!"}, 400
        user = UserModel(data['username'], data['email'], data['password'],
                         insert_timestamp())
        user.registered_timestamp = insert_timestamp()
        user.save_to_db()
        return {'message': "User created!"}, 201

class UserList(Resource):
    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}

class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        ItemModel.update_user_id(user_id)
        UserModel.delete_from_db(user)
        return {'message': 'User deleted.'}, 200

class UserGetItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username_email',
                        type=str,
                        required=True,
                        help="Every User needs a NAME"
                        )
    parser.add_argument('item_name',
                        type=str,
                        required=False,
                        help="Every Store needs a NAME"
                        )

    @jwt_required()
    def get(self):
        data = UserGetItem.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
            if not user:
                return {'message': 'User or Item not found'}, 404
        return user.json_item()

    @jwt_required()
    def post(self):
        data = UserGetItem.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = User.find_by_email(data['username_email'])
        item = ItemModel.find_by_name(data['item_name'])
        if not user or not item:
            return {'message': 'User or Item not found'}, 404
        item.user_id = user.id
        item.save_to_db()
        return {'message': "Item- '{}' is now IN '{}'s CART".format(item.item_name, user.username)}

    @jwt_required()
    def delete(self):
        data = UserGetItem.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
        item = ItemModel.find_by_name(data['item_name'])
        if not user or not item:
            return {'message': 'User or Item not found'}, 404
        item.user_id = None
        item.save_to_db()
        return {'message': "Item- '{}' is now DELETED '{}'s CART".format(item.item_name, user.username)}

class UserCart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username_email',
                        type=str,
                        required=True,
                        help="Every User needs a USERNAME / EMAIL"
                        )

    def post(self):
        data = UserCart.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
        if not user:
            return {'message': 'User not found'}, 404
        return {'items': [item.json() for item in ItemModel.find_cart(user.id)]}

    def get(self):
        data = UserCart.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
        if not user:
            return {'message': 'User not found'}, 404
        return {
            'user_id': user.id,
            'total_value': ItemModel.sum_cart_by_user_id(user.id)
        }

