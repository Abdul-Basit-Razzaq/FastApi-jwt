from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# example: "postgresql://postgres:your_password@localhost:5432/FastJwt"
DATABASE_URL = "postgresql://postgres:password@localhost:5432/FastJwt"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
