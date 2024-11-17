# mypy: ignore-errors
from db import db


class Time(db.Model):
    __tablename__ = 'time'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    hour = db.Column(db.Integer, nullable=False)
    minute = db.Column(db.Integer, nullable=False)
    part_of_day = db.Column(db.String(36), nullable=False)
