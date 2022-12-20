from app_config import db
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime


class Hire(db.Model):
    __tablename__ = 'hire'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    auto_id = Column(Integer, ForeignKey('auto.id'))
    client_id = Column(Integer, ForeignKey('client.id'))
    price = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    auto = ''
    client = ''
    def __repr__(self):
        return f'<hire {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
