# mypy: ignore-errors
from db import db


class UserAnalytics(db.Model):
    __tablename__ = 'user_analysis'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    age = db.Column(db.String(10), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    channel = db.Column(db.String(36), nullable=False)
    product = db.Column(db.String(36), nullable=False)
    satisfaction = db.Column(db.Float, nullable=False)
