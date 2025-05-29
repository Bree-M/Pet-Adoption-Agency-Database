from sqlalchemy import Column, Integer, String, Date
from .base import Base

class Adopter(Base):
    __tablename__ = 'adopters'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20))
    address = Column(String(200))
    registration_date = Column(Date, nullable=False)
    
    def __repr__(self):
        return f"<Adopter(id={self.id}, name='{self.name}', email='{self.email}')>"