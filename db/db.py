import bcrypt
import pytz
from flask_sqlalchemy import SQLAlchemy
import datetime
from tzlocal import get_localzone

db = SQLAlchemy()


def insert_timestamp():
    user_timezone = pytz.timezone(get_localzone().zone)
    new_post_date = user_timezone.localize(datetime.datetime.now())
    return new_post_date.astimezone(pytz.utc).timestamp()

def convert_timestamp(timestamp):
    utc_date = pytz.utc.localize(datetime.datetime.utcfromtimestamp(timestamp))
    return str(utc_date.astimezone(pytz.timezone(get_localzone().zone)))

def encrypt(content):
    return bcrypt.hashpw(content.encode("UTF-8"), bcrypt.gensalt())

def decrypt(x, y):
    return bcrypt.checkpw(x.encode("UTF-8"), y)

