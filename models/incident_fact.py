# mypy: ignore-errors
from db import db

from .enums import ScalingLevelEnum


class IncidentFact(db.Model):
    __tablename__ = 'incident_fact'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    client_id = db.Column(db.String(36), db.ForeignKey('client.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('product.id'), nullable=False)
    date_id = db.Column(db.String(36), db.ForeignKey('date.id'), nullable=False)
    time_id = db.Column(db.Integer, db.ForeignKey('time.id'), nullable=False)
    risk_id = db.Column(db.String(36), db.ForeignKey('risk.id'), nullable=False)
    agent_id = db.Column(db.String(36), db.ForeignKey('agent.id'), nullable=False)
    channel_id = db.Column(db.String(36), db.ForeignKey('channel.id'), nullable=False)
    scaling_level = db.Column(db.Enum(ScalingLevelEnum), nullable=False)
    resolution_time = db.Column(db.Integer, nullable=False)  # in days

    # Relationships
    user = db.relationship('User', backref='incident_fact')
    client = db.relationship('Client', backref='incident_fact')
    product = db.relationship('Product', backref='incident_fact')
    date = db.relationship('Date', backref='incident_fact')
    time = db.relationship('Time', backref='incident_fact')
    risk = db.relationship('Risk', backref='incident_fact')
    agent = db.relationship('Agent', backref='incident_fact')
    channel = db.relationship('Channel', backref='incident_fact')
