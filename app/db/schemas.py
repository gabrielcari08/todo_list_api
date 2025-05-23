#Este archivo define los esquemas (modelos) de entrada y salida para las rutas de la API.

from pydantic import BaseModel, EmailStr

#Clase que define el esquema para crear un usuario.
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

#Clase que define el esquema la devolucion de usuario.
class UserRespone(BaseModel):
    id: int
    name: str
    email: EmailStr
    
    class Config:
        orm_mode = True
        
#Clase que define el esquema para la creacion de tareas.
class TaskCreate(BaseModel):
    title: str
    description: str
    
#Clase que define la devolucion de tarea.
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    
    class Config:
        orm_mode = True
        
#Define el esquema que vamos a usar cuando un usuario intente iniciar sesion.
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
#Este esquema define cómo será la respuesta con el token
class Token(BaseModel):
    access_token: str
    token_type: str