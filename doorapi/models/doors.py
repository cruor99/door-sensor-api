from doorapi.extensions import db
import datetime


class Doors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    device_reference = db.Column(db.String(80))
    device_status = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime, default=datetime.datetime.now)
