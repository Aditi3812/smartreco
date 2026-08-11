from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    echo=True,pool_pre_ping=True,       # Automatically tests stale connections before executing queries
    pool_recycle=300,         # Recycles connections every 5 minutes (300 seconds)
    pool_timeout=30,          # Time to wait for an available connection from pool
)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)