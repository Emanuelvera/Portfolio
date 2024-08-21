from config.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

# Modelo EmployeeDay
class EmployeeDay(Base):
    __tablename__ = 'employee_days'
    
    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    dia = Column(String)
    
    # Define la relación inversa
    employee = relationship("Employee", back_populates="days")

# Modelo Employee
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    nacimiento = Column(String)
    empresa = Column(String)
    ingreso = Column(String)
    puesto = Column(String)
    turno = Column(String)
    dias = Column(Text)  # Aquí almacenas días como texto, considera cambiar si necesitas más flexibilidad

    # Define la relación con EmployeeDay
    days = relationship("EmployeeDay", back_populates="employee")