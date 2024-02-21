from config.database import Base
from sqlalchemy import Column, Integer, String

#Entidad
class Empleado(Base):

    __tablename__ = "empleados"

    id         = Column (Integer, primary_key = True)
    Nombre     = Column (String)
    Apellido   = Column (String)
    Nacimiento = Column (String)
    Empresa    = Column (String)
    Ingreso    = Column (String)
    Puesto     = Column (String)


