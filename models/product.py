from db import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(500), nullable=False)