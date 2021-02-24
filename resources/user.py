from flask_jwt_extended import (jwt_required, get_raw_jwt,
                                get_jwt_identity, create_access_token,
                                jwt_refresh_token_required,
                                create_refresh_token, get_jwt_claims)
from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.blocklist import BlockListModel
from models.user import UserModel
from models.item import ItemModel
from db.db import insert_timestamp, decrypt

NOT_CONFIRMED_ERROR = "You have not confirmed registration, " \
                      "please check your email:    {}"

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
                        required=True,
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
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privilege required."}, 401
        return {'all_users': [user.json() for user in UserModel.query.all()]}


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privilege required."}, 401

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json()

    @classmethod
    @jwt_required
    def delete(cls, user_id: int):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privilege required."}, 401

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        block = BlockListModel.find_by_user_id(user_id=user_id)
        if block:
            return {"message": "User Already in Block List"}, 404
        block = BlockListModel(user_id, insert_timestamp())
        ItemModel.update_user_id(user_id)
        block.save_to_db()
        return {"message": "User in Block List."}, 200


class UserGetItem(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item_name',
                        type=str,
                        required=False,
                        help="Every Store needs a Name"
                        )

    @classmethod
    @jwt_required
    def post(cls):
        data = UserGetItem.parser.parse_args()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        item = ItemModel.find_by_name(data['item_name'])
        if not item:
            return {"message": "Item not found"}, 404
        if item.store_id is None:
            return {"message": "Item is still OUT OF STOCK"}, 401
        item.user_id = user.id
        item.save_to_db()
        return {"message": "Item: {} been added to Cart".format(
            item.item_name,)}

    @classmethod
    @jwt_required
    def delete(cls):
        data = UserGetItem.parser.parse_args()
        item = ItemModel.find_by_name(data['item_name'])
        if not item:
            return {"message": "Item not found."}, 404
        item.user_id = None
        item.save_to_db()
        return {"message": "Item: {} is DELETED from Cart.".format(
            item.item_name,)}


class UserCart(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        return {user_id: [{
            'items': [item.json() for item in ItemModel.find_cart(user_id)],
            'total_quantity': ItemModel.count_cart_by_user_id(user_id),
            'total_value': ItemModel.sum_cart_by_user_id(user_id)
        }]}


class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username_email',
                        type=str,
                        required=True,
                        help="Every User needs a Username / Email."
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="Every User needs a Password."
                        )

    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if user is None:
            user = UserModel.find_by_email(data['username_email'])
        if user and decrypt(data['password'], user.password):
            if user.activated:
                if (BlockListModel.find_by_user_id(user.id)) is None:
                    user.last_login_timestamp = insert_timestamp()
                    user.save_to_db()
                    access_token = create_access_token(identity=user.id, fresh=True)
                    refresh_token = create_refresh_token(user.id)
                    return {"access_token": access_token,
                            "refresh_token": refresh_token}, 200
            return {'message': NOT_CONFIRMED_ERROR.format(user.email)}, 400
        return {"message": "invalid credentials"}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "User successfully logged out."}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def get(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(current_user, fresh=False)
        return {"access_token": new_token}, 200

class UserConf(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found."}, 404
        user.activated = True
        user.save_to_db()
        return {"message": "User confirmed."}, 200

