# mypy: ignore-errors
from db import db

from .enums import DayOfWeekEnum


class Date(db.Model):
    __tablename__ = 'date'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    day = db.Column(db.String(36), nullable=False)
    month = db.Column(db.String(36), nullable=False)
    quarter = db.Column(db.String(36), nullable=False)
    year = db.Column(db.String(36), nullable=False)
    day_of_week = db.Column(db.Enum(DayOfWeekEnum), nullable=False)
