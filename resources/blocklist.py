from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims
from db.db import insert_timestamp
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

    @classmethod
    @jwt_required
    def post(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
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

    @classmethod
    @jwt_required
    def delete(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
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
    @classmethod
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        return {'users': [user.json() for user in BlockListModel.query.all()]}