from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# In production, use pooled connections for high concurrency
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Checks connection health before using
    pool_size=20,  # Number of permanent connections
    max_overflow=10,  # Extra connections during spikes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
