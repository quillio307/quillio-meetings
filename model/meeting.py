from datetime import datetime as dt
from setup import db
from model.user import User


class Meeting(db.Document):
    name = db.StringField(required=True, min_length=3, max_length=50)
    members = db.ListField(db.ReferenceField(User))
    active = db.BooleanField()
    created_at = db.DateTimeField(default=dt.now())
    meta = {'strict': False}
