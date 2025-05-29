from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base

class Adoption(Base):
    __tablename__ = 'adoptions'
    
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey('pets.id'), nullable=False)
    adopter_id = Column(Integer, ForeignKey('adopters.id'), nullable=False)
    adoption_date = Column(Date, nullable=False)
    
    pet = relationship("Pet", backref="adoptions")
    adopter = relationship("Adopter", backref="adoptions")
    
    def __repr__(self):
        return f"<Adoption(id={self.id}, pet_id={self.pet_id}, adopter_id={self.adopter_id})>"