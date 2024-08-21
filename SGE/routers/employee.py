from fastapi import APIRouter
from fastapi import Path, HTTPException, Depends
from fastapi.responses import  JSONResponse
from typing import  List
from config.database import Session
from models.employee import Employee as EmployeeModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.employee import EmployeeService
from schemas.employee import Employee

employee_router = APIRouter()


#FUNCIONES



#Trae todos los employees

@employee_router.get('/employees', tags = ["employees"], response_model= List[Employee], status_code = 200)
def get_employees()-> List[Employee]:
    db = Session()
    result = EmployeeService(db).get_employees()
    return JSONResponse (status_code = 200, content = jsonable_encoder(result))


#Filtro de employees // queda pendiente conectarlo con la db
@employee_router.get('/employees/filter', tags=["employees"], response_model=List[Employee], status_code=200)
def get_employee(id: int | None = None, nombre: str | None = None, apellido: str | None = None,
                 nacimiento: str | None = None, empresa: str | None = None, ingreso: str | None = None,
                 puesto: str | None = None) -> List[Employee]:
    db = Session()

    result = EmployeeService(db).get_employee(
        id=id, nombre=nombre, apellido=apellido, nacimiento=nacimiento, empresa=empresa, ingreso=ingreso, puesto=puesto
    )

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Employees no encontrados")

    
#Creacion de employees

@employee_router.post('/employees', tags=["employees"], response_model=dict, status_code=201)
def add_employee(employee: Employee) -> dict:
    db = Session()
    
    try:
        # Crear una instancia del servicio
        employee_service = EmployeeService(db)
        
        # Agregar el empleado y los días de trabajo
        employee_service.add_employee(employee)
        
        # Devolver respuesta exitosa
        return JSONResponse(
            status_code=201,
            content={"message": "El empleado se ha registrado correctamente"}
        )
    finally:
        db.close()
#@employee_router.post ('/employees',tags=["employees"], response_model= dict, status_code = 201, dependencies = [Depends(JWTBearer())])


#Hacer modificaciones en los employees

@employee_router.put('/employees/{id}', tags=["employees"], response_model=dict, status_code=200)
def modify_employees(id: int, employee: Employee) -> dict:
    db = Session()
    employee_service = EmployeeService(db)
    
    existing_employee = employee_service.get_employee(id)
    if not existing_employee:
        return JSONResponse(status_code=404, content={"message": "No se encontró ningún empleado"})

    employee_service.modify_employees(id, employee)

    return JSONResponse(status_code=200, content={"message": "El empleado se ha modificado correctamente"})


#Eliminar employees

@employee_router.delete('/employees/{id}', tags=["employees"], response_model= dict, status_code = 200, dependencies = [Depends(JWTBearer())])
def delete_employee(id : int = Path(ge=1, le=2000)) -> dict:
    db = Session()
    result:EmployeeModel = db.query(EmployeeModel).filter(EmployeeModel.id == id).first()
    if not result:
        return JSONResponse (status_code=404, content={"message" : "No se encontro ningun employee"})
    EmployeeService(db).delete_employee(id)    
    return JSONResponse (status_code = 200, content = {"message" : "El employee se ha eliminado correctamente"})



@employee_router.get('/employees/{id}', tags=["employees"], response_model=Employee, status_code=200)
def get_employee_by_id(id: int = Path(..., title="ID del Employee a buscar")) -> Employee:
    db = Session()

    employee = EmployeeService(db).get_employee_by_id(id)

    if employee:
        return employee
    else:
        raise HTTPException(status_code=404, detail="Employee no encontrado")

