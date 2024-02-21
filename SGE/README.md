# Proyecto de Gestión de Empleados

Este proyecto consiste en una aplicación web para gestionar empleados. A continuación, se detallan los pasos necesarios para ejecutarla en tu entorno local.

## Instrucciones de Ejecución

### Clonar el Repositorio
Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/Emanuelvera/Portfolio.git
```

### Activar el Entorno Virtual

Accede a la carpeta del proyecto y activa el entorno virtual. Dependiendo de tu sistema operativo, ejecuta uno de los siguientes comandos:

#### Linux:

```bash
cd SGE
source sge-env/bin/activate
```

#### Windows:

```bash
cd SGE
sge-env\Scripts\activate
```

### Instalar Dependencias
Una vez activado el entorno virtual, instala las dependencias del proyecto:

```bash
Copy code
pip3 install -r requirements.txt
```

### Ejecutar la Aplicación
Con todas las dependencias instaladas, puedes ejecutar la aplicación con el siguiente comando:

```bash
uvicorn main:app --port 5000 --reload
```

### Acceder a la Aplicación

Finalmente, abre tu navegador web y accede a la siguiente dirección:
http://127.0.0.1:5000

Puedes ver la documentacion del mismo desde:
http://127.0.0.1:5000/docs