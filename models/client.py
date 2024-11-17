# mypy: ignore-errors
from db import db

from .enums import PlanEnum


class Client(db.Model):
    __tablename__ = 'client'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    plan = db.Column(db.Enum(PlanEnum), nullable=False)
    initial_date = db.Column(db.Date, nullable=False)
    final_date = db.Column(db.Date, nullable=False)
