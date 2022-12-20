from app_config import db
from sqlalchemy import Column, Integer, String, BigInteger



class Client(db.Model):
    __tablename__ = 'client'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    vu = Column(Integer, nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    birthday = Column(Integer,  nullable=False)
    phone = Column(BigInteger, nullable=False, unique=True)

    def __repr__(self):
        return f'<client {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
