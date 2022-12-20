from app_config import db
from sqlalchemy import Column, Integer, String, ForeignKey


class Violations(db.Model):
    __tablename__ = 'violations'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    hire_id = Column(Integer, ForeignKey('hire.id'))
    description = Column(String(1500), nullable=False)

    def __repr__(self):
        return f'<violations {self.id}>'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
