from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from flask_restful import Resource, reqparse
from models.user import UserModel
from db.db import insert_timestamp, encrypt, decrypt

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
    @jwt_required
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        UserModel.delete_from_db(user)
        return {'message': 'User deleted.'}, 200

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username_email',
                        type=str,
                        required=True,
                        help="this field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="this field cannot be blank.")

    def post(self):
        data = UserLogin.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
            if not user:
                return {'message': 'Invalid credentials1'}, 401
        if user and decrypt(data['password'], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                   }, 200
        return {'message': 'Invalid credentials2'}, 401
