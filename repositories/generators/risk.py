import secrets
from uuid import uuid4

from db import db
from models import Risk
from models.enums import RiskLevelEnum
from repositories import RiskRepository


class GeneratorRiskRepository(RiskRepository):
    def __init__(self) -> None:
        self.db = db

    def populate_table(self) -> None:
        risks = []
        risk_1 = Risk(id=str(uuid4()), risk_level=RiskLevelEnum.LOW.value)
        risks.append(risk_1)

        risk_2 = Risk(id=str(uuid4()), risk_level=RiskLevelEnum.MEDIUM.value)
        risks.append(risk_2)

        risk_3 = Risk(id=str(uuid4()), risk_level=RiskLevelEnum.HIGH.value)
        risks.append(risk_3)

        self.db.session.add_all(risks)
        self.db.session.commit()

    def get_random_risk(self) -> Risk:
        risks = self.db.session.query(Risk).all()
        return secrets.choice(risks)

    def delete_all_risks(self) -> None:
        self.db.session.query(Risk).delete()
        self.db.session.commit()
