# # from sqlalchemy import create_engine
# # from sqlalchemy.orm import sessionmaker, declarative_base
# # from dotenv import load_dotenv
# # import os
# # load_dotenv()
# # DATABASE_URL = os.getenv("DATABASE_URL")
# # engine = create_engine(DATABASE_URL, future=True)
# # SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
# #
# # Base = declarative_base()
# #
# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from dotenv import load_dotenv
# import os
#
# # Load environment variables from .env file
# load_dotenv()
#
# # Get the database URL from environment variables
# DATABASE_URL = os.getenv("DATABASE_URL")
#
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL is not set in the environment variables.")
#
# # Create the database engine
# engine = create_engine(
#     DATABASE_URL,
#     connect_args={"sslmode": "require"}  # Required by Railway PostgreSQL
# )
# # Create a session factory
# SessionLocal = sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
#     future=True
# )
#
# # Base class for declarative models
# Base = declarative_base()
#
# # Dependency to get a database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables.")

# Create engine for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    connect_args={"sslmode": "require"}  # For Railway PostgreSQL
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

