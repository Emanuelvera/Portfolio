from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()

app.title = "SGE (Sistema de Gestion de Empleados)"
app.version = "0.0.1"


class Empleado(BaseModel):
    id         : Optional[int] = None
    Nombre     : str = Field (max_length=30)
    Apellido   : str = Field (max_length=30)
    Nacimiento : str = Field(max_length=8, min_length=8)
    Empresa    : str = Field (max_length=10)
    Ingreso    : str = Field(max_length=8, min_length=8)
    Puesto     : str = Field (max_length=20)

    class Config:
        json_schema_extra  = {
            "example":{
                "id"         : 1,
                "Nombre"     : "Ingrese Nombre",
                "Apellido"   : "Ingrese apellido",
                "Nacimiento" : "Ingrese fecha con formato XX/XX/XXXX",
                "Empresa"    : "Ingrese Empresa",
                "Ingreso"    : "Ingrese fecha con formato XX/XX/XXXX",
                "Puesto"     : "Ingrese Puesto",
            }
        }




empleados = [
    {
        'id'         : 1,
        'Nombre'     : 'Juan',
        'Apellido'   : 'Pessini',
        'Nacimiento' : '05/02/1998',
        'Empresa'    : 'NyC',
        'Ingreso'    : '01/08/2023',
        'Puesto'     : 'Proximity'
    },
    {
        'id'         : 2,
        'Nombre'     : 'Marcos',
        'Apellido'   : 'Ludueña',
        'Nacimiento' : '05/02/1998',
        'Empresa'    : 'NyC',
        'Ingreso'    : '01/08/2023',
        'Puesto'     : 'Proximity'
    },
    {
        'id'         : 3,
        'Nombre'     : 'Jeremias',
        'Apellido'   : 'De souza',
        'Nacimiento' : '05/02/1998',
        'Empresa'    : 'NPO',
        'Ingreso'    : '01/08/2023',
        'Puesto'     : 'Proximity'
    }
]
    




#FUNCIONES


#Pagina de inicio

@app.get("/", tags = ["home"])
def message():
    return HTMLResponse("<h1>SGE</h1><h2>Nuevo empleado</h2><h2>Editar empleado</h2><h2>Eliminar empleado</h2>")


#Trae todos los empleados

@app.get('/empleados', tags = ["empleados"], response_model= List[Empleado], status_code = 200)
def get_empleados()-> List[Empleado]:
    return JSONResponse (status_code = 200, content = empleados)

#Filtro de empleados

@app.get('/empleados/filter', tags = ["empleados"],response_model= Empleado, status_code = 200)
def get_empleado(id:int | None = None, Nombre:str| None = None, Apellido:str| None = None, Nacimiento:str| None = None, Empresa:str| None = None, Ingreso:str| None = None, Puesto:str| None = None)-> Empleado:
    for item in empleados:
        for key, value in item.items():
            if locals().get(key) is not None and value != locals()[key]:
                break
        else:
            return JSONResponse (status_code = 200, content = item)
        
    return JSONResponse (status_code=404,content=[])

#Creacion de empleados

@app.post ('/empleados',tags=["empleados"], response_model= dict, status_code = 201)
def crear_empleado(empleado: Empleado)->dict:
    empleados.append(empleado)
    return JSONResponse (status_code = 201, content = {"El empleado se ha registrado correctamente"})

#Hacer modificaciones en los empleados

@app.put('/empleados/{id}', tags=["empleados"], response_model= dict, status_code = 200)
def modificar_empleados(id : int, empleado : Empleado) -> dict:
    for item in empleados:
        if item ["id"] == id:
            item["Nombre"] = empleado.Nombre
            item["Apellido"] = empleado.Apellido
            item["Nacimiento"] = empleado.Nacimiento
            item["Empresa"] = empleado.Empresa
            item["Ingreso"] = empleado.Ingreso
            item["Puesto"] = empleado.Puesto
            return JSONResponse (status_code = 200, content = {"El empleado se ha modificado correctamente"})
        else:
            return JSONResponse(status_code = 404, content= [])
        

@app.delete('/empleados/{id}', tags=["empleados"], response_model= dict, status_code = 200)
def eliminar_empleado(id : int = Path(ge=1, le=2000)) -> dict:
    for item in empleados:
        if item["id"] == id:
            empleados.remove(item)
            return JSONResponse (status_code = 200, content = {"El empleado se ha eliminado correctamente"})
        else:
            return JSONResponse(status_code = 404, content= [])
        
        
        




                        