from models.empleado import Empleado as EmpleadoModel
from schemas.empleado import Empleado


class EmpleadoService():

    def __init__(self, db) -> None:
        self.db = db

    def get_empleados(self):
        result = self.db.query(EmpleadoModel).all()
        return result
    
    def get_empleado(self, id:int | None = None, nombre:str| None = None, apellido:str| None = None, nacimiento:str| None = None, empresa:str| None = None, ingreso:str| None = None, puesto:str| None = None):
         
        filters = {
        'id': id,
        'nombre': nombre,
        'apellido': apellido,
        'nacimiento': nacimiento,
        'empresa': empresa,
        'ingreso': ingreso,
        'puesto': puesto,
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
         
        empleado.nombre = data.nombre
        empleado.apellido = data.apellido
        empleado.nacimiento = data.nacimiento
        empleado.empresa = data.empresa
        empleado.ingreso = data.ingreso
        empleado.puesto = data.puesto

        self.db.commit()
        return 
    
    def eliminar_empleado(self, id : int):
    
        self.db.query(EmpleadoModel).filter(EmpleadoModel.id == id).delete()
        self.db.commit()
        return

        
     