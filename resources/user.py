from models.user import UserModel
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
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
    @jwt_required()
    def delete(self, content):
        user = UserModel.find_by_id(content)
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'}
        return {'message': 'user not found'}, 400


