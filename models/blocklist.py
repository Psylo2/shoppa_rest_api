from typing import Dict, Union
from db.db import db, convert_timestamp

BlockJSON = Dict[int, Union[int, float]]

class BlockListModel(db.Model):
    __tablename__ = 'blocklist'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, unique=True)
    insert_time = db.Column(db.Float)

    def __init__(self, user_id: int, insert_time: float):
        self.user_id = user_id
        self.insert_time = insert_time

    def json(self) -> BlockJSON:
        return {self.id: [{'user_id': self.user_id,
                           'insert_time': convert_timestamp(self.insert_time)}]
                }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, user_id: int) -> "BlockListModel":
        return cls.query.filter_by(user_id=user_id).first()




