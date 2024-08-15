from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from config.database import Session, engine, Base
from middlewares.error_handler import ErrorHandler
from routers.employee import  employee_router, modify_employees
from routers.user import user_router
from schemas.employee import Employee
from schemas.user import User
from services.employee import EmployeeService
from routers.user import login as user_login 
import json

app = FastAPI()

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de Jinja2
templates = Jinja2Templates(directory="templates")

# Configuración de Swagger
app.title = "SGE (Sistema de Gestión de Empleados)"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(employee_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)

# Configuración de CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


# Página de logueo
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#Autenticacion
@app.post("/", response_class=RedirectResponse)
async def login(email: str = Form(...), password: str = Form(...)):
    user = User(email=email, password=password)
    
    # Llama a la función de login en el router y obtén la respuesta
    response = user_login(user)
    
    if response.status_code == 200:
        token_dict = json.loads(response.body.decode("utf-8"))

        # Redirecciona a la página de inicio después de la autenticación exitosa
        redirect_response = RedirectResponse(url="/index", status_code=303)
        redirect_response.set_cookie(key="access_token", value=token_dict, httponly=True)
        return redirect_response
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Página de inicio después de la autenticación
@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    db = Session()
    employee_service = EmployeeService(db)
    employees = employee_service.get_employee()
    return templates.TemplateResponse("index.html", {"request": request, "employees": employees})

#Creacion de usuario
@app.post("/add_employee", response_class=HTMLResponse)
async def add_employee(
    request: Request,
    nombre: str = Form(...), 
    apellido: str = Form(...), 
    nacimiento: str = Form(...), 
    empresa: str = Form(...), 
    ingreso: str = Form(...), 
    puesto: str = Form(...)
):
    # Crear un diccionario con los datos recibidos
    employee_data = {
        "nombre": nombre,
        "apellido": apellido,
        "nacimiento": nacimiento,
        "empresa": empresa,
        "ingreso": ingreso,
        "puesto": puesto
    }

    # Crear el objeto Employee usando Pydantic
    employee = Employee(**employee_data)

    # Crear una sesión de base de datos y el servicio de empleado
    db = Session()
    employee_service = EmployeeService(db)
    
    # Agregar el empleado
    employee_service.add_employee(employee)
    
    # Redirigir después de la inserción
    return RedirectResponse("/index", status_code=303)


#Eliminacion de usuario
@app.post("/delete-employee/{id}", response_class=HTMLResponse)
def delete_employees(id: int):
    db = Session()
    employee_service = EmployeeService(db)
    employee_service.delete_employee(id)
    return RedirectResponse(url="/index", status_code=303)


#Edicion de usuario
@app.get("/edit-employee/{id}", response_class=HTMLResponse)
async def edit_employee(request: Request, id: int):
    db = Session()
    employee_service = EmployeeService(db)
    employee = employee_service.get_employee_by_id(id)
    
    if not employee:
        return HTMLResponse(content="Empleado no encontrado", status_code=404)


    return templates.TemplateResponse("edit-employee.html", {"request": request, "employee": employee})


@app.post("/employees/{id}", response_class=HTMLResponse)
async def modify_employee(request: Request, id: int, nombre: str = Form(...), apellido: str = Form(...), nacimiento: str = Form(...), empresa: str = Form(...), ingreso: str = Form(...), puesto: str = Form(...)):

    employee_data = Employee(
        nombre=nombre,
        apellido=apellido,
        nacimiento=nacimiento,
        empresa=empresa,
        ingreso=ingreso,
        puesto=puesto
    )

    response = modify_employees(id, employee_data)
    
    if response.status_code == 200:
        return RedirectResponse("/index", status_code=303)
    else:
        raise HTTPException(status_code=response.status_code, detail="No se pudo modificar el empleado.")
