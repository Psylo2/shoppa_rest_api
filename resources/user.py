from security import crypt
from models.user import UserModel
from flask_restful import Resource, reqparse
from db.db import insert_timestamp

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="this field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="this field cannot be blank.")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "Username already Taken!"}, 400

        user = UserModel(data['username'], crypt(data['password'].encode('UTF-8')), insert_timestamp())
        user.save_to_db()
        return {'message': "User created!"}, 201

class UserList(Resource):
    def get(self):
        return {'users': [user.json() for user in UserModel.query.all()]}
