# mypy: ignore-errors
from db import db

from .enums import ChannelEnum


class Channel(db.Model):
    id = db.Column(db.String(36), primary_key=True, nullable=False)
    channel_type = db.Column(db.Enum(ChannelEnum), nullable=False)
