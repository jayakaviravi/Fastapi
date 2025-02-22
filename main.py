from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .database import SessionLocal, engine

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# EMPLOYEE
@app.post('/employees/', response_model=schemas.Employee, tags=['Employee'])
def create_employee(request: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    new_employee = models.Employee(name=request.name, email=request.email, designation=request.designation, payroll=request.payroll)
    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)
    return new_employee

@app.get('/employees/', response_model=List[schemas.Employee], tags=['Employee'])
def get_employees(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    employees = db.query(models.Employee).offset(skip).limit(limit).all()
    return employees

@app.get('/employees/{employee_id}', status_code=200, response_model=schemas.Employee, tags=['Employee'])
def show_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Employee with id {employee_id} not found')
    return employee

@app.delete('/employees/{employee_id}', status_code=status.HTTP_200_OK, tags=['Employee'])
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    deleted = db.query(models.Employee).filter(models.Employee.id == employee_id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with id {employee_id} not found")
    return {"message": "Employee deleted successfully"}

@app.put('/employees/{employee_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Employee'])
def update_employee(employee_id: int, request: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    for key, value in request.dict().items():
        setattr(db_employee, key, value)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# PROJECT

@app.post('/projects/', response_model=schemas.Project, tags=['Project'])
def create_project(request: schemas.ProjectCreate, db: Session = Depends(get_db)):
    new_project = models.Project(title=request.title, description=request.description)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@app.get('/projects/', response_model=List[schemas.Project], tags=['Project'])
def get_projects(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    projects = db.query(models.Project).offset(skip).limit(limit).all()
    return projects

@app.get('/projects/{project_id}', status_code=200, response_model=schemas.Project, tags=['Project'])
def show_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Project with id {project_id} not found')
    return project

@app.delete('/projects/{project_id}', status_code=status.HTTP_200_OK, tags=['Project'])
def delete_project(project_id: int, db: Session = Depends(get_db)):
    deleted = db.query(models.Project).filter(models.Project.id == project_id).delete(synchronize_session=False)
    db.commit()
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Project with id {project_id} not found")
    return {"message": "Project deleted successfully"}

@app.put('/projects/{project_id}', status_code=status.HTTP_202_ACCEPTED, tags=['Project'])
def update_project(project_id: int, request: schemas.ProjectCreate, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    for key, value in request.dict().items():
        setattr(db_project, key, value)
    db.commit()
    db.refresh(db_project)
    return db_project

# Assigning  Employees to Projects

@app.post('/projects/{project_id}/employees/{employee_id}', tags=['Assignment'])
def assign_employee_to_project(project_id: int, employee_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not project or not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project or Employee not found")
    project.employees.append(employee)
    db.commit()
    return {"message": "Employee assigned to project successfully"}

@app.post('/employees/{employee_id}/projects/{project_id}', tags=['Assignment'])
def assign_project_to_employee(employee_id: int, project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not project or not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project or Employee not found")
    employee.projects.append(project)
    db.commit()
    return {"message": "Project assigned to employee successfully"}

# To Get employee with projects
@app.get('/employees/{employee_id}/projects/', response_model=schemas.EmployeeWithProjects, tags=['Employee'])
def get_employee_projects(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return employee

# To Get project with employees
@app.get('/projects/{project_id}/employees/', response_model=schemas.ProjectWithEmployees, tags=['Project'])
def get_project_employees(project_id: int, db: Session = Depends(get_db)):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

