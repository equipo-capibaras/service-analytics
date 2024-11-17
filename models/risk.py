# mypy: ignore-errors
from db import db

from .enums import RiskLevelEnum


class Risk(db.Model):
    __tablename__ = 'risk'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    risk_level = db.Column(db.Enum(RiskLevelEnum), nullable=False)
