from typing import List
from pydantic import BaseModel

class EmployeeBase(BaseModel):
    name: str
    email: str
    designation: str
    payroll: str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int
    projects: List["Project"] = []

    class Config:
        from_attributes = True

class ProjectBase(BaseModel):
    title: str
    description: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    employee_id: int

    class Config:
        from_attributes = True
