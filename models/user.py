from db.db import db, convert_timestamp, encrypt

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.LargeBinary)
    email = db.Column(db.String(20), unique=True)
    registered_timestamp = db.Column(db.Float)
    last_login_timestamp = db.Column(db.Float)
    bin_username = db.Column(db.LargeBinary)
    bin_email = db.Column(db.LargeBinary)

    def __init__(self, username, email, password, registered_timestamp):
        self.username = username
        self.email = email
        self.password = password
        self.registered_timestamp = registered_timestamp
        self.bin_username = encrypt(username)
        self.bin_email = encrypt(email)

    def json(self):
        return {'id': self.id, 'bin_username': str(self.bin_username), 'password': str(self.password),
                'bin_email': str(self.bin_email), 'registered_at': convert_timestamp(self.registered_timestamp),
                'username': self.username, 'email': self.email}

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
