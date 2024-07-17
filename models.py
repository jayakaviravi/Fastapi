from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Employee(Base):
    __tablename__ = 'employees'
    
    id: int = Column(Integer, primary_key=True, index=True)
    name: str = Column(String, index=True)
    email: str = Column(String, unique=True, index=True)
    designation: str = Column(String, index=True)
    payroll: str = Column(String)
    
    projects = relationship("Project", back_populates="employee")

class Project(Base):
    __tablename__ = 'projects'
    
    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, index=True)
    description: str = Column(String, index=True)
    employee_id: int = Column(Integer, ForeignKey('employees.id'))
    
    employee = relationship("Employee", back_populates="projects")
