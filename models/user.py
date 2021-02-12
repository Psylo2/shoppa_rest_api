from db.db import db, convert_timestamp

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    registered_timestamp = db.Column(db.Float)

    def __init__(self, username, password, registered_timestamp):
        self.username = username
        self.password = password
        self.registered_timestamp = registered_timestamp


    def json(self):
        return {'username': self.username, 'password': str(self.password),
                'registered_at': convert_timestamp(self.registered_timestamp)}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()