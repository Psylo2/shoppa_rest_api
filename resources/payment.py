from flask_restful import Resource
from flask_jwt_extended import get_jwt_identity, fresh_jwt_required
from db.db import insert_timestamp
from models.payment import PaymentModel
from models.item import ItemModel

class Payment(Resource):
    @classmethod
    @fresh_jwt_required
    def post(cls):
        user_id = get_jwt_identity()
        value = ItemModel.sum_cart_by_user_id(user_id)
        if value and value != 0:
            quantity = ItemModel.count_cart_by_user_id(user_id)
            payment = PaymentModel(user_id, value, quantity, insert_timestamp())
            payment.save_to_db()
            ItemModel.update_user_id(user_id)
            return {"message": "Payment ACCEPTED"}, 200
        else:
            return {"message": "No Items in Cart!"}, 401

    @classmethod
    @fresh_jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        return {
            'user_id': user_id,
            'items': [item.json() for item in ItemModel.find_cart(user_id)],
            'total_quantity': ItemModel.count_cart_by_user_id(user_id),
            'total_value': ItemModel.sum_cart_by_user_id(user_id)
        }

class PaymentList(Resource):
    @classmethod
    @fresh_jwt_required
    def get(cls):
        return {'all_payments': [payment.json() for payment in PaymentModel.query.all()]}
