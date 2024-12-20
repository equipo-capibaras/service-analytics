# mypy: ignore-errors
from db import db

from .enums import ProductTypeEnum


class Product(db.Model):  # type: ignore[name-defined]
    __tablename__ = 'product'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum(ProductTypeEnum), nullable=False)
    description = db.Column(db.String(500), nullable=False)
