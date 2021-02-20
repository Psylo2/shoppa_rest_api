from flask_restful import Resource, reqparse
from db.db import insert_timestamp


from flask_jwt import jwt_required

from models.blocklist import BlockListModel
from models.item import ItemModel
from models.user import UserModel


class BlockList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username_email',
                        type=str,
                        required=True,
                        help="Every User needs a USERNAME / EMAIL"
                        )

    @jwt_required()
    def post(self):
        data = BlockList.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
        if not user:
            return {'message': 'User not found'}, 404
        block = BlockListModel.find_by_user_id(user_id=user.id)
        if block:
            return {'message': 'User already in block list'}, 404
        block = BlockListModel(user.id, insert_timestamp())
        ItemModel.update_user_id(user.id)
        block.save_to_db()
        return {'message': "User- '{}' is now in Block List".format(user.username)}

    @jwt_required()
    def delete(self):
        data = BlockList.parser.parse_args()
        user = UserModel.find_by_username(data['username_email'])
        if not user:
            user = UserModel.find_by_email(data['username_email'])
        if not user:
            return {'message': 'User not found'}, 404
        block = BlockListModel.find_by_user_id(user_id=user.id)
        if not block:
            return {'message': 'User not found in block list'}, 404
        block.delete_from_db()
        return {'message': "User- '{}' is now in Deleted from Block List".format(user.username)}


class BlockListShow(Resource):
    @jwt_required()
    def get(self):
        return {'users': [user.json() for user in BlockListModel.query.all()]}