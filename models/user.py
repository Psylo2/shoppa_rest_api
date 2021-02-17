from db.db import db, convert_timestamp, encrypt


class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.LargeBinary)
    email = db.Column(db.String(20), unique=True)
    registered_timestamp = db.Column(db.Float)
    last_login_timestamp = db.Column(db.Float)
    hash_username = db.Column(db.LargeBinary)
    hash_email = db.Column(db.LargeBinary)

    def __init__(self, username, email, password, registered_timestamp):
        self.username = username
        self.email = email
        self.password = encrypt(password)
        self.registered_timestamp = registered_timestamp
        self.hash_username = encrypt(username)
        self.hash_email = encrypt(email)

    def json(self):
        return {'id': self.id, 'hash_username': str(self.hash_username), 'password': str(self.password),
                'hash_email': str(self.hash_email), 'registered_at': convert_timestamp(self.registered_timestamp),
                'username': self.username, 'email': self.email}

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
