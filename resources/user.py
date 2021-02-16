from models.user import UserModel
from flask_restful import Resource, reqparse
from db.db import insert_timestamp, encrypt

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=False)
    parser.add_argument('email', type=str, required=False)
    parser.add_argument('password', type=str, required=True, help="this field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "Username already Taken!"}, 400
        if UserModel.find_by_email(data['email']):
            return {"message": "Email already Taken!"}, 400

        user = UserModel(data['username'], data['email'], encrypt(data['password']), insert_timestamp())
        user.save_to_db()
        return {'message': "User created!"}, 201

class UserList(Resource):
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
        user.delete_from_db(user_id)
        return {'message': 'User deleted.'}, 200

