from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db import models
from auth import hashing, jwt_handler
from db.schemas import Token, UserLogin
from db.models import User
from auth.jwt_handler import create_access_token
from auth.hashing import Hash

router = APIRouter(prefix="/auth", tags=["authentication"])

#Maneja la creacion de la sesion de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Endpoint de prueba
@router.get("/")
async def hello_router():
    return {"Hello": "Auth"}

#Enpoint para logear usuario y retornar un token
@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    #Buscamos en la base de datos si el email del usuario coincide con el ingresado
    user = db.query(User).filter(User.email == user_credentials.email).first()
    
    #Si no existe el usuario lanzamos una excepcion.
    if not user:
        raise HTTPException(
            status_code=404,    
            detail="Credenciales incorrectas"
        )
        
    #Verificamos que la contraseña almacenada coincida con la ingresada.
    if not Hash.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=404,    
            detail="Credenciales incorrectas"
        )
    
    #Si todo es correcto, generamos el token con el id del usuario.
    acces_token = create_access_token(data={"user_id": user.id})
    
    #Retornamos el token JWT
    return {"access_token": acces_token, "token_type": "bearer"}
        
    