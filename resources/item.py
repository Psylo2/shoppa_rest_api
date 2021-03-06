from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required, get_jwt_claims
from db.db import insert_timestamp
from models.item import ItemModel
from models.store import StoreModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('item_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('price',
                        type=float,
                        required=False,
                        help="This field cannot be left blank!"
                        )

    @classmethod
    @jwt_required
    def get(cls, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            return item.json()
        return {"message": "Item not found"}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls):
        data = Item.parser.parse_args()
        if ItemModel.find_by_name(data['item_name']):
            return {'message': "item {} already exists.".format(data['item_name'])}
        data = Item.parser.parse_args()
        item = ItemModel(data['item_name'], data['price'], insert_timestamp())
        item.created_timestamp = insert_timestamp()
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the Item."}, 500
        return item.json(), 201

    @classmethod
    @jwt_required
    def delete(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privilege required."}, 401

        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(data['item_name'])
        if item and (item.user_id is None):
            item.delete_from_db()
            return {"message": "Item deleted"}
        return {"message": "Item is either taken by user or not found."}, 401

    @classmethod
    @jwt_required
    def put(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
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


class ItemAllList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privilege required."}, 401
        return {'all_items': [item.all_items_json() for item in ItemModel.query.all()]}

class ItemStockList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {'in_stock': [item.json() for item in ItemModel.find_stock()]}


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

    @classmethod
    @jwt_required
    def post(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = ItemToStore.parser.parse_args()
        store = StoreModel.find_by_name(data['store_name'])
        item = ItemModel.find_by_name(data['item_name'])
        if not store or not item:
            return {'message': 'Store or Item not found'}, 404
        item.store_id = store.id
        item.save_to_db()
        return {'message': "Item: {} is now IN STOCK".format(item.item_name,)}

    @classmethod
    @jwt_required
    def delete(cls):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message': 'Admin privilege required.'}, 401
        data = ItemToStore.parser.parse_args()
        store = StoreModel.find_by_name(data['store_name'])
        item = ItemModel.find_by_name(data['item_name'])
        if not store or not item:
            return {'message': 'Store not found'}, 404
        item.store_id = None
        item.save_to_db()
        return {'message': "Item: {} is now OUT OF STOCK".format(item.item_name,)}
