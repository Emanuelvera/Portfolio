from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

app.title = "SGE (Sistema de Gestion de Empleados)"
app.version = "0.0.1"



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

@app.get("/empleados", tags = ["empleados"])
def get_empleados():
    return empleados

#Filtro de empleados

@app.get('/empleados/filter', tags = ["empleados"])
def get_empleado(id:int | None = None, Nombre:str| None = None, Apellido:str| None = None, Nacimiento:str| None = None, Empresa:str| None = None, Ingreso:str| None = None, Puesto:str| None = None):
    for item in empleados:
        for key, value in item.items():
            if locals().get(key) is not None and value != locals()[key]:
                break
        else:
            return item
        
    return []