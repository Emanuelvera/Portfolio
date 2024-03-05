from fastapi import APIRouter
from fastapi import Path, Query, HTTPException, Depends
from fastapi.responses import  JSONResponse
from typing import  Optional, List
from config.database import Session
from models.empleado import Empleado as EmpleadoModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.empleado import EmpleadoService
from schemas.empleado import Empleado

empleado_router = APIRouter()


#FUNCIONES



#Trae todos los empleados

@empleado_router.get('/empleados', tags = ["empleados"], response_model= List[Empleado], status_code = 200)
def get_empleados()-> List[Empleado]:
    db = Session()
    result = EmpleadoService(db).get_empleados()
    return JSONResponse (status_code = 200, content = jsonable_encoder(result))


#Filtro de empleados // queda pendiente conectarlo con la db
@empleado_router.get('/empleados/filter', tags=["empleados"], response_model=List[Empleado], status_code=200)
def get_empleado(id: int | None = None, nombre: str | None = None, apellido: str | None = None,
                 nacimiento: str | None = None, empresa: str | None = None, ingreso: str | None = None,
                 puesto: str | None = None) -> List[Empleado]:
    db = Session()

    result = EmpleadoService(db).get_empleado(
        id=id, nombre=nombre, apellido=apellido, nacimiento=nacimiento, empresa=empresa, ingreso=ingreso, puesto=puesto
    )

    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail="Empleados no encontrados")

    
#Creacion de empleados

@empleado_router.post ('/empleados',tags=["empleados"], response_model= dict, status_code = 201, dependencies = [Depends(JWTBearer())])
def crear_empleado(empleado: Empleado)->dict:
    db = Session()
    EmpleadoService(db).crear_empleado(empleado)
    return JSONResponse (status_code = 201, content = {"message" : "El empleado se ha registrado correctamente"})


#Hacer modificaciones en los empleados

@empleado_router.put('/empleados/{id}', tags=["empleados"], response_model= Empleado, status_code = 200, dependencies = [Depends(JWTBearer())])
def modificar_empleados(id : int, empleado : Empleado, ) -> Empleado:
    db = Session()

    result = EmpleadoService(db).get_empleado(id)
    if not result:
        return JSONResponse (status_code=404, content={"message" : "No se encontro ningun empleado"})
    EmpleadoService(db).modificar_empleados(id, empleado)

    return JSONResponse (status_code = 200, content = {"message" : "El empleado se ha modificado correctamente"})


#Eliminar empleados

@empleado_router.delete('/empleados/{id}', tags=["empleados"], response_model= dict, status_code = 200, dependencies = [Depends(JWTBearer())])
def eliminar_empleado(id : int = Path(ge=1, le=2000)) -> dict:
    db = Session()
    result:EmpleadoModel = db.query(EmpleadoModel).filter(EmpleadoModel.id == id).first()
    if not result:
        return JSONResponse (status_code=404, content={"message" : "No se encontro ningun empleado"})
    EmpleadoService(db).eliminar_empleado(id)    
    return JSONResponse (status_code = 200, content = {"message" : "El empleado se ha eliminado correctamente"})



@empleado_router.get('/empleados/{id}', tags=["empleados"], response_model=Empleado, status_code=200, dependencies = [Depends(JWTBearer())])
def get_empleado_by_id(id: int = Path(..., title="ID del Empleado a buscar")) -> Empleado:
    db = Session()

    empleado = EmpleadoService(db).get_empleado_by_id(id)

    if empleado:
        return empleado
    else:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

