from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
 
class usuario(BaseModel):
    id: str = Field(..., example='u1')
    nombre: str= Field(..., example='Juan')
    email: EmailStr = Field(..., example='juan.perez@example.com')
    edad: int= Field(..., example=28)
 
 
class proyecto(BaseModel):
    id: str = Field(..., example='p1')
    nombre: str= Field(..., example='GDEMP-1000')
    descripcion: str= Field(..., example='Proyecto 1')
    id_usuario: str= Field(..., example='u1')