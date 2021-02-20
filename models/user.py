from db.db import db, convert_timestamp, encrypt

class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.LargeBinary)
    email = db.Column(db.String(25), unique=True)
    registered_timestamp = db.Column(db.Float)
    last_login_timestamp = db.Column(db.Float)


    def __init__(self, username: str, email: str, password: str, last_login_timestamp: float):
        self.username = username
        self.email = email
        self.password = encrypt(password)
        self.last_login_timestamp = last_login_timestamp

    def json(self) :
        return {'id': self.id, 'username': str(encrypt(self.username)),
                'email': str(encrypt(self.email)), 'password': str(self.password),
                'registered_at': convert_timestamp(self.registered_timestamp),
                'last_login_timestamp ': convert_timestamp(self.last_login_timestamp)}

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()


