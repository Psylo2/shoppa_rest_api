from sqlalchemy import func
from typing import Dict, Union, List
from db.db import db, convert_timestamp
from models.item import ItemModel, ItemJSON

PaymentJSON = Dict[int, Union[int, int, int, float, List[ItemJSON]]]

class PaymentModel(db.Model):
    __tablename__ = 'payment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(20))
    total_value = db.Column(db.Float(precision=2))
    total_quantity = db.Column(db.Integer)
    payment_timestamp = db.Column(db.Float)
    receipt = db.Column(db.Integer, autoincrement=True, unique=True)

    def __init__(self, user_id: int, total_value: float,
                 total_quantity: int, payment_timestamp: float):
        self.user_id = user_id
        self.total_value = total_value
        self.total_quantity = total_quantity
        self.payment_timestamp = payment_timestamp

    def json(self) -> PaymentJSON:
        return {self.id: [{
            'receipt_num': self.receipt,
            'user_id': self.user_id,
            'total_quantity': self.total_quantity,
            'total_value': self.total_value,
            'items': [item.json() for item in ItemModel.find_cart(self.id)]}]
        }

    @classmethod
    def find_by_user_id(cls, _id: int) -> "PaymentModel":
        return cls.query.with_entities(
            func.sum(convert_timestamp(PaymentModel.payment_timestamp))
        ).filter_by(user_id=_id).first()

    @classmethod
    def find_by_receipt(cls, num: int) -> "PaymentModel":
        return cls.query.filter_by(receipt=num).first()

    @classmethod
    def find_all_by_user_id(cls, _id: int) -> "PaymentModel":
        return cls.query.filter_by(user_id=_id).all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
