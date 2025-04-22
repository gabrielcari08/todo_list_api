from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from db.models import User
from db.database import SessionLocal
from db.schemas import UserCreate, UserRespone
from auth.hashing import Hash

router = APIRouter(prefix="/users", tags=["users"])

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
    return {"Hello": "Router"}

#Endpoint para registrar un nuevo usuario en la base de datos
@router.post("/register", response_model=UserRespone)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    #Buscamos en la base de datos para comprobar si el usuario existe comprobando emails
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    #Si existe, lanzamos una excepcion
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="El usuario ya existe"
        )
    
    #Hasheamos la contraseña antes de almacenarla en la base de datos.
    hashed_password = Hash.bcrypt(user.password)
    
    #Creamos una nueva instancia de User.
    new_user = User(
        name = user.name,
        email = user.email,
        password = hashed_password
    )
    
    #Agregamos el objeto new_user a la base de datos
    db.add(new_user)
    #Guardamos los cambios
    db.commit()
    #Refrescamos la base de datos
    db.refresh(new_user)
    
    #Retornamos el usuario creado
    return new_user