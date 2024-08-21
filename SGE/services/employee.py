import json
from models.employee import Employee as EmployeeModel, EmployeeDay
from schemas.employee import Employee


class EmployeeService():

    def __init__(self, db) -> None:
        self.db = db

    def get_employees(self):
        result = self.db.query(EmployeeModel).all()
        return result
    
    def get_employee(self, id:int | None = None, nombre:str| None = None, apellido:str| None = None, nacimiento:str| None = None, empresa:str| None = None, ingreso:str| None = None, puesto:str| None = None, turno:str| None = None, dias:str| None = None):
         
        filters = {
        'id': id,
        'nombre': nombre,
        'apellido': apellido,
        'nacimiento': nacimiento,
        'empresa': empresa,
        'ingreso': ingreso,
        'puesto': puesto,
        'turno': turno,
        'dias': dias,
        # ... otros filtros ...
        }

        query_filters = {key: value for key, value in filters.items() if value is not None}
        filtered_employees = [employee for employee in self.db.query(EmployeeModel) if all(getattr(employee, field) == value for field, value in query_filters.items())]
        return filtered_employees
    
    def add_employee(self, employee: Employee):
        # Convierte la lista de días a una cadena JSON
        dias_json = json.dumps(employee.dias)
        
        # Crea el nuevo empleado
        new_employee = EmployeeModel(
            nombre=employee.nombre,
            apellido=employee.apellido,
            nacimiento=employee.nacimiento,
            empresa=employee.empresa,
            ingreso=employee.ingreso,
            puesto=employee.puesto,
            turno=employee.turno,
            dias=dias_json
        )
        
        self.db.add(new_employee)
        self.db.commit()

        # Crea entradas en la tabla EmployeeDay para cada día de la lista
        for dia in employee.dias:
            employee_day = EmployeeDay(employee_id=new_employee.id, dia=dia)
            self.db.add(employee_day)
        
        self.db.commit()
    
    def modify_employees(self, id : int, data : Employee):
    
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == id).first()
        employee.nombre = data.nombre
        employee.apellido = data.apellido
        employee.nacimiento = data.nacimiento
        employee.empresa = data.empresa
        employee.ingreso = data.ingreso
        employee.puesto = data.puesto
        employee.turno = data.turno
        
        # Convierte la lista de días en una cadena JSON
        employee.dias = json.dumps(data.dias)
        self.db.commit()
        return 
    
    def get_employee_by_id(self, id: int) -> EmployeeModel:
        employee = self.db.query(EmployeeModel).filter(EmployeeModel.id == id).first()
        if employee:
        # Convierte la cadena JSON de vuelta a una lista
            employee.dias = json.loads(employee.dias)
            return employee
    
    def delete_employee(self, id : int):
    
        self.db.query(EmployeeModel).filter(EmployeeModel.id == id).delete()
        self.db.commit()
        return

        
     