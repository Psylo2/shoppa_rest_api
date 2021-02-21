from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from db.db import insert_timestamp
from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('price',
                        type=float,
                        required=False,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(data['item_name']):
            return {'message': "An item with name '{}' already exists.".format(data['item_name'])}
        data = Item.parser.parse_args()
        item = ItemModel(data['item_name'], data['price'], insert_timestamp())
        item.created_timestamp = insert_timestamp()
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the Item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(data['item_name'])
        if item and (item.user_id is None):
            item.delete_from_db()
            return {'message': 'Item deleted'}
        return {"message": "Item is either taken by user or not found."}, 401

    @jwt_required()
    def put(self):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(data['item_name'])
        if item is None:
            item = ItemModel(data['item_name'], data['price'], insert_timestamp())
            item.created_timestamp = insert_timestamp()
        else:
            item.price = data['price']
            item.modify_timestamp = insert_timestamp()
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}


class ItemToStore(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('store_name',
                        type=str,
                        required=True,
                        help="Every Store needs a NAME"
                        )
    parser.add_argument('item_name',
                        type=str,
                        required=False,
                        help="Every Item needs a NAME"
                        )

    @jwt_required()
    def post(self):
        data = ItemToStore.parser.parse_args()
        store = StoreModel.find_by_name(data['store_name'])
        item = ItemModel.find_by_name(data['item_name'])
        if not store or not item:
            return {'message': 'Store or Item not found'}, 404
        item.store_id = store.id
        item.save_to_db()
        return {'message': "Item '{}' is now IN STOCK at store '{}'".format(item.item_name,
                                                                            store.name)}
    @jwt_required()
    def delete(self):
        data = ItemToStore.parser.parse_args()
        store = StoreModel.find_by_name(data['store_name'])
        item = ItemModel.find_by_name(data['item_name'])
        if not store or not item:
            return {'message': 'Store not found'}, 404
        item.store_id = None
        item.save_to_db()
        return {'message': "Item '{}' is now OUT OF STOCK at store '{}'".format(item.item_name,
                                                                                store.name)}
