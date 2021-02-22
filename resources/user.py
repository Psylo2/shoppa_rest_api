from flask import jsonify
from flask_jwt_extended import jwt_required, get_raw_jwt, get_jwt_identity, create_access_token, \
    jwt_refresh_token_required, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask_restful import Resource, reqparse

from blacklist import BLACKLIST
from models.blocklist import BlockListModel
from security import auth_by_username
from models.user import UserModel
from models.item import ItemModel
from db.db import insert_timestamp

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
    @classmethod
    def post(cls):
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
    @classmethod
    def get(cls):
        return {'users': [user.json() for user in UserModel.query.all()]}

class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    @jwt_required
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

    @classmethod
    @jwt_required
    def get(cls):
        data = UserGetItem.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
            if not user:
                return {'message': 'User or Item not found'}, 404
        return user.json_item()

    @classmethod
    @jwt_required
    def post(cls):
        data = UserGetItem.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
        item = ItemModel.find_by_name(data['item_name'])
        if not user or not item:
            return {'message': 'User or Item not found'}, 404
        if item.store_id is None:
            return {'message': 'Item is still OUT OF STOCK'}, 401
        item.user_id = user.id
        item.save_to_db()
        return {'message': "Item- '{}' is now IN '{}'s CART".format(
            item.item_name, user.username)}

    @classmethod
    @jwt_required
    def delete(cls):
        data = UserGetItem.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
        item = ItemModel.find_by_name(data['item_name'])
        if not user or not item:
            return {'message': 'User or Item not found'}, 404
        item.user_id = None
        item.save_to_db()
        return {'message': "Item- '{}' is now DELETED '{}'s CART".format(
            item.item_name, user.username)}

class UserCart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username_email',
                        type=str,
                        required=True,
                        help="Every User needs a USERNAME / EMAIL"
                        )

    @classmethod
    @jwt_required
    def get(cls):
        data = UserCart.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
        if not user:
            return {'message': 'User not found'}, 404
        return {user.id: [{
            'items': [item.json() for item in ItemModel.find_cart(user.id)],
            'total_quantity': ItemModel.count_cart_by_user_id(user.id),
            'total_value': ItemModel.sum_cart_by_user_id(user.id)
        }]}


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username_email',
                        type=str,
                        required=True,
                        help="Every User needs a USERNAME / EMAIL"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Every User needs a USERNAME / EMAIL"
                        )

    @classmethod
    def post(cls):
        data = UserLogin.parser.parse_args()
        user = auth_by_username(data['username_email'], data['password'])
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)
        # access_cookies = set_access_cookies(access_token)
        # refresh_cookies = set_refresh_cookies(refresh_token)
        return {"access_token": access_token, "refresh_token": refresh_token}, 200

class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return "User id: {} successfully logged out.".format(user_id)

class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(current_user, fresh=False)
        return {'access_token': new_token}, 200

