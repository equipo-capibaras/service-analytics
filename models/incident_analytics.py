# mypy: ignore-errors
from db import db


class IncidentAnalytics(db.Model):
    __tablename__ = 'incident_analysis'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    user_name = db.Column(db.String(250), nullable=False)
    user_age = db.Column(db.Integer, nullable=False)
    user_city = db.Column(db.String(80), nullable=False)
    user_country = db.Column(db.String(80), nullable=False)
    user_continent = db.Column(db.String(80), nullable=False)
    user_language = db.Column(db.String(80), nullable=False)
    client_name = db.Column(db.String(80), nullable=False)
    client_plan = db.Column(db.String(80), nullable=False)
    product_name = db.Column(db.String(80), nullable=False)
    product_type = db.Column(db.String(80), nullable=False)
    product_description = db.Column(db.String(500), nullable=False)
    date_day = db.Column(db.String(36), nullable=False)
    date_month = db.Column(db.String(36), nullable=False)
    date_quarter = db.Column(db.String(36), nullable=False)
    date_year = db.Column(db.String(36), nullable=False)
    date_day_of_week = db.Column(db.String(50), nullable=False)
    time_hour = db.Column(db.Integer, nullable=False)
    time_minute = db.Column(db.Integer, nullable=False)
    time_part_of_day = db.Column(db.String(50), nullable=False)
    risk_level = db.Column(db.String(50), nullable=False)
    agent_name = db.Column(db.String(80), nullable=False)
    agent_experience = db.Column(db.Integer, nullable=False)
    channel_type = db.Column(db.String(80), nullable=False)
    scaling_level = db.Column(db.Integer, nullable=False)
    resolution_time = db.Column(db.Integer, nullable=False)  # in hours
