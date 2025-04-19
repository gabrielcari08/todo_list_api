#Este archivo se encarga de definir la estructura de las tablas de la base de datos.

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from .database import engine

Base = declarative_base()

#Tabla de usuarios
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    #Relación con tareas (un usuario tiene muchas tareas)
    tasks = relationship("Task", back_populates="owner")
    
#Tabla de tareas
class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    
    #Clave foránea: esta tarea pertenece a un usuario
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    #Relación con el usuario (una tarea tiene un dueño)
    owner = relationship("User", back_populates="tasks")