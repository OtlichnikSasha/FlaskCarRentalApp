from app_config import db
from sqlalchemy import Column, Integer, String


class Auto(db.Model):
    __tablename__ = 'auto'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    gos_number = Column(String(255), nullable=False, unique=True)
    vin = Column(String(255), nullable=False, unique=True)
    issue_year = Column(Integer, nullable=False)
    mark = Column(String(255), nullable=False)
    model = Column(String(1024), nullable=False)
    color = Column(String(60), nullable=False)
    price = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<auto {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
