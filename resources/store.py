from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models.store import StoreModle
from db.db import insert_timestamp

class Store(Resource):
    @jwt_required()
    def get(self, name):
        store = StoreModle.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModle.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400
        store = StoreModle(name, insert_timestamp(), insert_timestamp())
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModle.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Store deleted.'}


class StoreList(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.json() for store in StoreModle.query.all()]}