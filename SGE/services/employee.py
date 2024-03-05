from models.employee import Employee as EmployeeModel
from schemas.employee import Employee


class EmployeeService():

    def __init__(self, db) -> None:
        self.db = db

    def get_employees(self):
        result = self.db.query(EmployeeModel).all()
        return result
    
    def get_employee(self, id:int | None = None, nombre:str| None = None, apellido:str| None = None, nacimiento:str| None = None, empresa:str| None = None, ingreso:str| None = None, puesto:str| None = None):
         
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

        query_filters = {key: value for key, value in filters.items() if value is not None}
        filtered_employees = [employee for employee in self.db.query(EmployeeModel) if all(getattr(employee, field) == value for field, value in query_filters.items())]
        return filtered_employees
    
    def crear_employee(self, employee: Employee):
        new_employee = EmployeeModel(**employee.dict())
        self.db.add(new_employee)
        self.db.commit()
        return 
    
    def modificar_employees(self, id : int, data : Employee):
    
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == id).first()
         
        employee.nombre = data.nombre
        employee.apellido = data.apellido
        employee.nacimiento = data.nacimiento
        employee.empresa = data.empresa
        employee.ingreso = data.ingreso
        employee.puesto = data.puesto

        self.db.commit()
        return 
    
    def get_employee_by_id(self, id: int) -> EmployeeModel:
        return self.db.query(EmployeeModel).filter(EmployeeModel.id == id).first()
    
    def eliminar_employee(self, id : int):
    
        self.db.query(EmployeeModel).filter(EmployeeModel.id == id).delete()
        self.db.commit()
        return

        
     