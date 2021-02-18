from db.db import db, convert_timestamp, encrypt

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.LargeBinary)
    email = db.Column(db.String(25), unique=True)
    registered_timestamp = db.Column(db.Float)
    last_login_timestamp = db.Column(db.Float)

    def __init__(self, username, email, password, last_login_timestamp):
        self.username = username
        self.email = email
        self.password = encrypt(password)
        self.last_login_timestamp = last_login_timestamp

    def json(self):
        return {'id': self.id, 'username': str(encrypt(self.username)),
                'email': str(encrypt(self.email)), 'password': str(self.password),
                'registered_at': convert_timestamp(self.registered_timestamp),
                'last_login_timestamp ': convert_timestamp(self.last_login_timestamp)}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
