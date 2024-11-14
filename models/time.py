from db import db
from .enums import PartOfDayEnum

class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    part_of_day = db.Column(db.Enum(PartOfDayEnum), nullable=False)