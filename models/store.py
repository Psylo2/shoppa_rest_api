from typing import Dict
from db.db import db, convert_timestamp

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    created_timestamp = db.Column(db.Float)
    modify_timestamp = db.Column(db.Float)

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name: str, created_timestamp: float, modify_timestamp: float):
        self.name = name
        self.created_timestamp = created_timestamp
        self.modify_timestamp = modify_timestamp


    def json(self) -> "Dict":
        return {'id': self.id, 'name': self.name,
                'created_at': convert_timestamp(self.created_timestamp),
                'last_modified': convert_timestamp(self.modify_timestamp),
                'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name: str) -> "StoreModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id: str) -> "StoreModel":
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()




