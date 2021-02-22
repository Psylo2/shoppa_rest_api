from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from db.db import insert_timestamp
from models.payment import PaymentModel
from models.item import ItemModel
from models.user import UserModel

class Payment(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('user_id',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @classmethod
    @jwt_required
    def post(cls):
        data = Payment.parser.parse_args()
        user = UserModel.find_by_username(data['user_id'])
        if not user:
            user = UserModel.find_by_email(data['user_id'])
            if not user:
                return {'message': 'User or Item not found'}, 404
        value = ItemModel.sum_cart_by_user_id(user.id)
        if value and value != 0:
            quantity = ItemModel.count_cart_by_user_id(user.id)
            payment = PaymentModel(user.id, value, quantity, insert_timestamp)
            payment.save_to_db()
            ItemModel.update_user_id(user.id)
            return {
                'message': 'Payment ACCEPTED'
            }, 200
        else:
            return{
                'message': 'No Items in Cart!'
                  }, 401

    @classmethod
    @jwt_required
    def get(cls):
        data = Payment.parser.parse_args()
        user = UserModel.find_by_username(data['user_id'])
        if not user:
            user = UserModel.find_by_email(data['user_id'])
        if not user:
            return {'message': 'User not found'}, 404
        return {
            'user_id': user.id,
            'items': [item.json() for item in ItemModel.find_cart(user.id)],
            'total_quantity': ItemModel.count_cart_by_user_id(user.id),
            'total_value': ItemModel.sum_cart_by_user_id(user.id)
        }

class PaymentList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        return {'users': [payment.json() for payment in PaymentModel.query.all()]}
