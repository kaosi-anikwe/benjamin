from datetime import datetime

# local imports
from . import db

# timestamp to be inherited by other class models
class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def format_update_date(self):
        return (
            self.updated_at.strftime("%d %B, %Y %I:%M:%S")
            if self.updated_at
            else None
        )
    def format_create_date(self):
        return self.created_at.strftime("%d %B, %Y %I:%M:%S")


# db helper functions
class DatabaseHelperMixin(object):
    def update(self):
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class ButtonStatus(db.Model, TimestampMixin, DatabaseHelperMixin):
    __tablename__ = "button_status"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)
    hardware_id = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(1024))

    def __init__(self, status, hardware_id, message=""):
        self.status = status
        self.hardware_id = hardware_id
        self.message = message

    def format(self):
        return {
            "hardware_id": self.hardware_id,
            "status": self.status,
            "message": self.message,
            "created_at": self.format_create_date(),
            "updated_at": self.format_update_date(),
        }


class Devices(db.Model, TimestampMixin, DatabaseHelperMixin):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True)
    hardware_id = db.Column(db.String(200), nullable=False)
    enabled = db.Column(db.Boolean, default=True)

    def __init__(self, hardware_id):
        self.hardware_id = hardware_id
