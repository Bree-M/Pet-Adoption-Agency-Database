from sqlalchemy import Column, Integer, String, Date, Enum
from .base import Base

class Pet(Base):
    __tablename__ = 'pets'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    species = Column(Enum('dog', 'cat', 'bird', 'rabbit', 'other'), nullable=False)
    breed = Column(String(50))
    age = Column(Integer)
    arrival_date = Column(Date, nullable=False)
    adopted = Column(Integer, default=0)  # 0 for not adopted, 1 for adopted
    
    def __repr__(self):
        return f"<Pet(id={self.id}, name='{self.name}', species='{self.species}')>"