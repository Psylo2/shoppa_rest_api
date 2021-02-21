import re
from sqlalchemy import func
from typing import Dict
from db.db import db, convert_timestamp

class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item_name = db.Column(db.String(20))
    price = db.Column(db.Float(precision=2))
    created_timestamp = db.Column(db.Float)
    modify_timestamp = db.Column(db.Float)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel')
    user_id = db.Column(db.Integer)

    def __init__(self, item_name: str, price: float, modify_timestamp: float):
        self.item_name = item_name
        self.price = price
        self.modify_timestamp = modify_timestamp

    def json(self) -> Dict:
        return {'id': self.id, 'item_name': self.item_name, 'price': self.price,
                'created_at': convert_timestamp(self.created_timestamp),
                'last_modified': convert_timestamp(self.modify_timestamp),
                'store_id': self.store_id, 'user_id': self.user_id}

    @classmethod
    def find_by_name(cls, item_name: str) -> "ItemModel":
        return cls.query.filter_by(item_name=item_name).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "ItemModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_cart(cls, _id: int) -> "ItemModel":
        return cls.query.filter_by(user_id=_id).all()

    @classmethod
    def update_user_id(cls, _id) -> "ItemModel":
        return cls.query.filter_by(user_id=_id).\
            update({ItemModel.user_id: None}).all()

    @classmethod
    def sum_cart_by_user_id(cls, _id: int) -> "ItemModel":
        tot = str(cls.query.with_entities(func.sum(ItemModel.price)).
                  filter_by(user_id=_id).all())
        fl = float(re.sub('[^0-9.]', '', tot))
        return round(fl, 2)

    @classmethod
    def count_cart_by_user_id(cls, _id: int) -> "ItemModel":
        count = str(cls.query.with_entities(func.count(ItemModel.price)).
                    filter_by(user_id=_id).all())
        return int(re.sub('[^0-9]', '', count))

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()




