// Login y redirección a index
    document.getElementById("login-button").addEventListener("click", function (event) {
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
            if (response.status === 200) {
                return response.json();
            } else {
                throw new Error("Invalid credentials");
            }
        })
        .then((data) => {
            localStorage.setItem("jwt_token", data.token);
            window.location.href = "/index";
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("Ocurrió un error al procesar tu solicitud. Inténtalo de nuevo más tarde.");
        });
    });


/*
function loadEmployees() {
    let token = localStorage.getItem("jwt_token");
    if (!token) {
        console.error("No se encontró el token JWT en el localStorage");
        return;
    }

    fetch("http://localhost:5000/employees", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error("Error al realizar la solicitud GET");
        }
    })
    .then(data => {
        const tableBody = document.getElementById("employee-table-body");
        tableBody.innerHTML = ''; // Limpiar la tabla antes de cargar los empleados

        data.forEach(employee => {
            const row = document.createElement("tr");

            const nameCell = document.createElement("td");
            nameCell.textContent = employee.nombre;
            row.appendChild(nameCell);

            const lastNameCell = document.createElement("td");
            lastNameCell.textContent = employee.apellido;
            row.appendChild(lastNameCell);

            const birthDateCell = document.createElement("td");
            birthDateCell.textContent = employee.nacimiento;
            row.appendChild(birthDateCell);

            const companyCell = document.createElement("td");
            companyCell.textContent = employee.empresa;
            row.appendChild(companyCell);

            const entryDateCell = document.createElement("td");
            entryDateCell.textContent = employee.ingreso;
            row.appendChild(entryDateCell);

            const positionCell = document.createElement("td");
            positionCell.textContent = employee.puesto;
            row.appendChild(positionCell);

            const operationsCell = document.createElement("td");

            const editLink = document.createElement("a");
            editLink.href = `/edit-employee/${employee.id}`;  // Enlace a la página de edición con el ID del empleado
            editLink.textContent = "Editar";
            editLink.addEventListener("click", function () {
                //editEmployee(employee.id);
            });
            operationsCell.appendChild(editLink);

            operationsCell.appendChild(document.createTextNode(" | ")); // Separador

            const deleteLink = document.createElement("a");
            deleteLink.href = "#";
            deleteLink.textContent = "Eliminar";
            deleteLink.addEventListener("click", function () {
                deleteEmployee(employee.id);
            });
            operationsCell.appendChild(deleteLink);

            row.appendChild(operationsCell);
            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error("Error:", error);
    });
}


function deleteEmployee(id) {
    let token = localStorage.getItem("jwt_token");
    if (!token) {
        console.error("No se encontró el token JWT en el localStorage");
        return;
    }

    fetch(`http://localhost:5000/employees/${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${token}`
        }
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else if (response.status === 404) {
            return response.json().then(data => {
                throw new Error(data.message);
            });
        } else {
            throw new Error("Error al eliminar el employee");
        }
    })
    .then(data => {
        console.log(data.message);
        alert(data.message);
        loadEmployees(); // Recargar empleados después de eliminar
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Ocurrió un error al procesar la solicitud.");
    });
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("create-employee-form").addEventListener("submit", function (event) {
        event.preventDefault();

        let nombre = document.querySelector('input[name="nombre"]').value;
        let apellido = document.querySelector('input[name="apellido"]').value;
        let nacimiento = document.querySelector('input[name="nacimiento"]').value;
        let empresa = document.querySelector('input[name="empresa"]').value;
        let ingreso = document.querySelector('input[name="ingreso"]').value;
        let puesto = document.querySelector('input[name="puesto"]').value;

        let employeeData = {
            nombre: nombre,
            apellido: apellido,
            nacimiento: nacimiento,
            empresa: empresa,
            ingreso: ingreso,
            puesto: puesto
        };

        let token = localStorage.getItem("jwt_token");
        if (!token) {
            console.error("No se encontró el token JWT en el localStorage");
            return;
        }

        fetch("http://localhost:5000/employees", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify(employeeData)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else if (response.status === 401) {
                throw new Error("No autenticado");
            } else {
                throw new Error("Error al crear el empleado");
            }
        })
        .then(data => {
            console.log(data.message);
            alert(data.message);
            loadEmployees(); // Recargar la lista de empleados después de añadir uno nuevo
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Ocurrió un error al procesar la solicitud.");
        });
    });
});*/
