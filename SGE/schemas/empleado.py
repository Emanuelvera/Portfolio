from pydantic import BaseModel, Field
from typing import  Optional, List




class Empleado(BaseModel):
    id         : Optional[int] = None
    nombre     : str = Field (max_length=30)
    apellido   : str = Field (max_length=30)
    nacimiento : str = Field(max_length=10, min_length=10)
    empresa    : str = Field (max_length=10)
    ingreso    : str = Field(max_length=10, min_length=10)
    puesto     : str = Field (max_length=20)

    class Config:
        json_schema_extra  = {
            "example":{
                "nombre"     : "Ingrese nombre",
                "apellido"   : "Ingrese apellido",
                "nacimiento" : "Ingrese fecha con formato XX/XX/XXXX",
                "empresa"    : "Ingrese empresa",
                "ingreso"    : "Ingrese fecha con formato XX/XX/XXXX",
                "puesto"     : "Ingrese puesto",
            }
        }
