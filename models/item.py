from db.db import db, convert_timestamp

class ItemModle(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    created_timestamp = db.Column(db.Float)
    modify_timestamp = db.Column(db.Float)

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relation('StoreModle')

    def __init__(self, item_name, price, created_timestamp, modify_timestamp, store_id):
        self.item_name = item_name
        self.price = price
        self.created_timestamp = created_timestamp
        self.modify_timestamp = modify_timestamp
        self.store_id = store_id


    def json(self):
        return {'item_name': self.item_name, 'price': self.price,
                'created_at': convert_timestamp(self.created_timestamp),
                'last_modified': convert_timestamp(self.modify_timestamp),
                'store_id': self.store_id}

    @classmethod
    def find_by_name(cls, item_name):
        return cls.query.filter_by(item_name=item_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()



