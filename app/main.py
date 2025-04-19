from fastapi import FastAPI
from sqlalchemy.orm import Session
from typing import List
from db import models
from db.models import Base, engine
from db.database import SessionLocal

app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
async def hello_fastapi():
    return {"message": "Hello!"}