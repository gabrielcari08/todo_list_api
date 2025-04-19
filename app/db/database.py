#Este archivo se encarga de crear la conexion a la base de datos y configurar la sesion.

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from .config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

url = URL.create(
    drivername="postgresql",
    username=(DB_USER),
    password=(DB_PASS),
    host=(DB_HOST),
    port=(DB_PORT),
    database=(DB_NAME)
)

engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

