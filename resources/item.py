from flask_restful import Resource, reqparse
from db.db import insert_timestamp
from models.item import ItemModel
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item need a store id"
                        )

    @jwt_required()
    def get(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, item_name):
        if ItemModel.find_by_name(item_name):
            return {'message': "An item with name '{}' already exists.".format(item_name)}
        data = Item.parser.parse_args()
        item = ItemModel(item_name, data['price'], insert_timestamp(), insert_timestamp(),
                         data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the Item."}, 500
        return item.json(), 201

    @jwt_required()
    def delete(self, item_name):
        item = ItemModel.find_by_name(item_name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}

    @jwt_required()
    def put(self, item_name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(item_name)
        if item is None:
            item = ItemModel(item_name, data['price'], insert_timestamp(), insert_timestamp(), data['store_id'])
        else:
            item.price = data['price']
            item.modify_timestamp = insert_timestamp()
            item.store_is = data['store_id']
        item.save_to_db()
        return item.json()

class ItemList(Resource):
    @jwt_required()
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}
