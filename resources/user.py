from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel
from db.db import insert_timestamp


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument()
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
        user = UserModel(data['username'], data['email'], data['password'], insert_timestamp())
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
        UserModel.delete_from_db(user)
        return {'message': 'User deleted.'}, 200
