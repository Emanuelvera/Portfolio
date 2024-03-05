from config.database import Base
from sqlalchemy import Column, Integer, String

#Entidad
class Employee(Base):

    __tablename__ = "employees"

    id         = Column (Integer, primary_key = True)
    nombre     = Column (String)
    apellido   = Column (String)
    nacimiento = Column (String)
    empresa    = Column (String)
    ingreso    = Column (String)
    puesto     = Column (String)

