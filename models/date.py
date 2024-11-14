from db import db

class Date(db.Model):
    __tablename__ = 'date'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    quarter = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.String(50), nullable=False)
    