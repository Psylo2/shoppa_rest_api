from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.store import StoreModel
from db.db import insert_timestamp

class Store(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_name',
                        type=str,
                        required=True,
                        help="Every Store needs a NAME"
                        )

    @classmethod
    @jwt_required
    def get(cls, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @classmethod
    @jwt_required
    def post(cls):
        data = Store.parser.parse_args()
        if StoreModel.find_by_name(data['store_name']):
            return {'message': "An item with name '{}' already exists.".format(
                data['store_name'])}, 400
        store = StoreModel(data['store_name'], insert_timestamp(), insert_timestamp())
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500
        return store.json(), 201

    @classmethod
    @jwt_required
    def delete(cls):
        data = Store.parser.parse_args()
        store = StoreModel.find_by_name(data['store_name'])
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted.'}


class StoreList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
