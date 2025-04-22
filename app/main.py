from fastapi import FastAPI
from routers import users, tasks, auth
from sqlalchemy.orm import Session
from typing import List
from db import models
from db.models import Base, engine
from db.database import SessionLocal

app = FastAPI()

#Routers

app.include_router(users.router)
app.include_router(tasks.router)
app.include_router(auth.router)

Base.metadata.create_all(engine)

@app.get("/")
async def hello_fastapi():
    return {"message": "Hello!"}