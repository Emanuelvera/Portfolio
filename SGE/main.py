from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.empleado import empleado_router
from routers.user import user_router

app = FastAPI()

app.title = "SGE (Sistema de Gestion de Empleados)"
app.version = "0.0.1"


app.add_middleware(ErrorHandler)
app.include_router(empleado_router)
app.include_router(user_router)


Base.metadata.create_all(bind = engine)



#Pagina de inicio

@app.get("/", tags = ["home"])
def message():
    return HTMLResponse("<h1>SGE</h1><h2>Nuevo empleado</h2><h2>Editar empleado</h2><h2>Eliminar empleado</h2>")



                        