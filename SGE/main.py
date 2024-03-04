from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.empleado import empleado_router
from routers.user import user_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.title = "SGE (Sistema de Gestion de Empleados)"
app.version = "0.0.1"


app.add_middleware(ErrorHandler)
app.include_router(empleado_router)
app.include_router(user_router)


Base.metadata.create_all(bind = engine)


# Configuración de CORS
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


#Pagina de inicio

@app.get("/", tags = ["home"], response_class=HTMLResponse)
async def message():
    html_content = """
    <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SGE - Sistema de Gestión de Usuarios</title>
    <!-- CSS -->
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f4;
      }
      .container {
        max-width: 1200px;
        margin: auto;
        padding: 20px;
      }
      .title {
        text-align: center;
        font-size: 36px;
        margin-bottom: 20px;
      }
      .login-box {
        background-color: #fff;
        border-radius: 8px;
        padding: 30px;
        padding-right: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        max-width: 400px;
        margin-left: auto;
        margin-right: auto;
      }
      input[type="text"],
      input[type="password"],
      input[type="submit"] {
        width: 90%;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #ccc;
        border-radius: 5px;
      }
      input[type="submit"] {
        background-color: #007bff;
        color: #fff;
        cursor: pointer;
      }
      .grid-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        grid-gap: 20px;
      }
      .card {
        background-color: #fff;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        text-align: center;
      }
    </style>
  </head>
  <!-- HTML -->
  <body>
    <div class="container">
      <h1 class="title">SGE - Sistema de Gestión de Empleados</h1>
      <div class="login-box" id="login-box">
        <h2>Iniciar sesión</h2>
        <form id="login-form" method="POST">
          <input type="text" name="email" placeholder="Correo electrónico" />
          <input type="password" name="password" placeholder="Contraseña" />
          <input id="login-button" type="submit" value="Iniciar sesión" />
        </form>
      </div>
      <div class="grid-container">
        <div class="card">
          <buttom><h2>Crear usuario </h2></buttom>
          <p>Aquí puedes crear un nuevo usuario.</p>
          <button type="button" id="post-empleado">create</button>
        </div>
        <div class="card">
          <buttom><h2>Buscar usuarios</h2></buttom>
          <p>Aquí puedes buscar usuarios existentes.</p>
          <button type="button" id="get-empleados">List All</button>
          <button type="button" id="get-empleado">Filter</button>
        </div>
        <div class="card">
          <buttom><h2>Modificar usuario</h2></buttom>
          <p>Aquí puedes modificar un usuario existente.</p>
          <button type="button" id="put-empleado">Modify</button>
        </div>
        <div class="card">
          <buttom><h2>Eliminar usuario</h2></buttom>
          <p>Aquí puedes eliminar un usuario existente.</p>
          <button type="button" id="delete-empleado">Delete</button>
        </div>
      </div>
    </div>


    <!-- JAVASCRIPT -->
    <script>
      document.addEventListener("DOMContentLoaded", function () {
    document
        .getElementById("login-button")
        .addEventListener("click", function () {
            event.preventDefault();
            let email = document.querySelector('input[name="email"]').value;
            let password = document.querySelector('input[name="password"]').value;

            var loginData = {
                email: email,
                password: password,
            };

            fetch("http://localhost:5000/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(loginData),
            })
                .then((response) => {
                    document.getElementById("login-box").style.display = "none";
                    return response.text(); // Convertir la respuesta a texto
                })
                .then((data) => {
                    localStorage.setItem("jwt_token", data.replace(/['"]+/g, '')); //Guarda el token en el local storage
                    console.log("Token JWT almacenado en el localStorage:", data);
                })
                .catch((error) => {
                    console.error("Error:", error);
                    alert("Ocurrió un error al procesar tu solicitud. Inténtalo de nuevo más tarde.");
                });
        });
});


      document.addEventListener("DOMContentLoaded", function () {
        document
          .getElementById("get-empleados")
          .addEventListener("click", function () {
            fetch("http://localhost:5000/empleados", {
              method: "GET",
            })
              .then((response) => {
                if (response.ok) {
                  return response.json();
                } else {
                  throw new Error("Error al realizar la solicitud GET");
                }
              })
              .then((data) => {
                console.log(data);
              })
              .catch((error) => {
                console.error("Error:", error);
              });
          });
      });

      document.addEventListener("DOMContentLoaded", function () {
    document
      .getElementById("delete-empleado")
      .addEventListener("click", function () {
        let token = localStorage.getItem("jwt_token"); // Obtener token JWT del localStorage
        if (!token) {
          console.error("No se encontró el token JWT en el localStorage");
          return;
        }

        let id = prompt("Ingrese el ID del empleado a eliminar:");
        if (!id) {
          return; // Si no se proporciona un ID, salimos de la función
        }

        fetch(`http://localhost:5000/empleados/${id}`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`, // Agregar el token JWT como header de autorización
          },
        })
          .then((response) => {
            if (response.ok) {
              console.log("Empleado eliminado correctamente");
            } else {
              throw new Error("Error al eliminar el empleado");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("Ocurrió un error al procesar la solicitud.");
          });
        });
      });
        
    document.addEventListener("DOMContentLoaded", function () {
    document
      .getElementById("post-empleado")
      .addEventListener("click", function () {
        let token = localStorage.getItem("jwt_token"); // Obtener token JWT del localStorage
        if (!token) {
          console.error("No se encontró el token JWT en el localStorage");
          return;
        }
        let nombre =  prompt("Ingrese el nombre del empleado a crear:");
        let apellido =  prompt("Ingrese el apellido del empleado a crear:");
        let nacimiento =  prompt("Ingrese el nacimiento del empleado a crear:");
        let empresa =  prompt("Ingrese el empresa del empleado a crear:");
        let ingreso =  prompt("Ingrese el ingreso del empleado a crear:");
        let puesto =  prompt("Ingrese el puesto del empleado a crear:");
        if (!nombre) {
          return; // Si no se proporciona un nombre, salimos de la función
        }

        fetch(`http://localhost:5000/empleados`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`, // Agregar el token JWT como header de autorización
          },
        })
          .then((response) => {
            if (response.ok) {
              console.log("Empleado creado correctamente");
            } else {
              throw new Error("Error al crear el empleado");
            }
          })
          .catch((error) => {
            console.error("Error:", error);
            alert("Ocurrió un error al procesar la solicitud.");
          });
        });
      });


      

    </script>
  </body>
</html>
    """
    return HTMLResponse(content=html_content,status_code=200)



                        