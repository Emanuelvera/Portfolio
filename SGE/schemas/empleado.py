from pydantic import BaseModel, Field
from typing import  Optional, List




class Empleado(BaseModel):
    id         : Optional[int] = None
    Nombre     : str = Field (max_length=30)
    Apellido   : str = Field (max_length=30)
    Nacimiento : str = Field(max_length=10, min_length=10)
    Empresa    : str = Field (max_length=10)
    Ingreso    : str = Field(max_length=10, min_length=10)
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
