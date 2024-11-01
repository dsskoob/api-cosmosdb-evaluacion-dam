from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
 
class Usuario(BaseModel):
    id: str = Field(..., example='u1')
    nombre: str= Field(..., example='Juan')
    email: EmailStr = Field(..., example='juan.perez@example.com')
    edad: int= Field(..., example=28)
 
 
class Proyecto(BaseModel):
    id: str = Field(..., example='p1')
    nombre: str= Field(..., example='GDEMP-1000')
    descripcion: str= Field(..., example='Proyecto 1')
    id_usuario: str= Field(..., example='u1')
    fecha_creacion: str = Field(..., example='2024-11-01T12:00:00Z')