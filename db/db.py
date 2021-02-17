import bcrypt
from flask_sqlalchemy import SQLAlchemy
import pytz
from tzlocal import get_localzone
import datetime
db = SQLAlchemy()

def insert_timestamp():
    user_timezone = pytz.timezone(get_localzone().zone)  # Asia/Jerusalem
    new_post_date = user_timezone.localize(datetime.datetime.now())  # GMT+2
    return new_post_date.astimezone(pytz.utc).timestamp()  # UTC timestamp

def convert_timestamp(timestamp):
    utc_date = pytz.utc.localize(datetime.datetime.utcfromtimestamp(timestamp))  # timestamp to UTC time
    return str(utc_date.astimezone(pytz.timezone(get_localzone().zone)))  # UTC to local time

def encrypt(x):
    return bcrypt.hashpw(x.encode("UTF-8"), bcrypt.gensalt(14))

def decrypt(x, y):
    return bcrypt.checkpw(x.encode("UTF-8"), y)
