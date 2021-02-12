from db.db import db, convert_timestamp

class StoreModle(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    created_timestamp = db.Column(db.Float)
    modify_timestamp = db.Column(db.Float)

    items = db.relationship('ItemModle', lazy='dynamic')

    def __init__(self, name, created_timestamp, modify_timestamp):
        self.name = name
        self.created_timestamp = created_timestamp
        self.modify_timestamp = modify_timestamp


    def json(self):
        return {'name': self.name, 'created_at': convert_timestamp(self.created_timestamp),
                'last_modified': convert_timestamp(self.modify_timestamp),
                'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




