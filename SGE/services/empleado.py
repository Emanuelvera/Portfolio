from models.empleado import Empleado as EmpleadoModel
from schemas.empleado import Empleado


class EmpleadoService():

    def __init__(self, db) -> None:
        self.db = db

    def get_empleados(self):
        result = self.db.query(EmpleadoModel).all()
        return result
    
    def get_empleado(self, id:int | None = None, Nombre:str| None = None, Apellido:str| None = None, Nacimiento:str| None = None, Empresa:str| None = None, Ingreso:str| None = None, Puesto:str| None = None):
         
        filters = {
        'id': id,
        'Nombre': Nombre,
        'Apellido': Apellido,
        'Nacimiento': Nacimiento,
        'Empresa': Empresa,
        'Ingreso': Ingreso,
        'Puesto': Puesto,
        # ... otros filtros ...
        }

        result = self.db.query(EmpleadoModel).filter(
            *[getattr(EmpleadoModel, field) == value for field, value in filters.items() if value is not None]
        )
        return result
    
    def crear_empleado(self, empleado: Empleado):
        new_empleado = EmpleadoModel(**empleado.dict())
        self.db.add(new_empleado)
        self.db.commit()
        return 
    
    def modificar_empleados(self, id : int, data : Empleado):
    
        empleado = self.db.query(EmpleadoModel).filter(EmpleadoModel.id == id).first()
         
        empleado.Nombre = data.Nombre
        empleado.Apellido = data.Apellido
        empleado.Nacimiento = data.Nacimiento
        empleado.Empresa = data.Empresa
        empleado.Ingreso = data.Ingreso
        empleado.Puesto = data.Puesto

        self.db.commit()
        return 
    
    def eliminar_empleado(self, id : int):
    
        self.db.query(EmpleadoModel).filter(EmpleadoModel.id == id).delete()
        self.db.commit()
        return

        
     