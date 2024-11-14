from db import db

class Agent(db.Model):
    __tablename__ = 'agent'

    id = db.Column(db.String(36), primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    experience = db.Column(db.Integer, nullable=False)





