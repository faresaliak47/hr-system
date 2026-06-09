from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database.models import Base
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'hr.db')
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# expire_on_commit=False prevents stale-data issues after commit/rerun cycles
engine = create_engine(
    f'sqlite:///{DB_PATH}',
    echo=False,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,   # ← FIX: prevents stale reads after commit
)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db() -> Session:
    """Return a fresh database session. Caller MUST call db.close() in a finally block."""
    return SessionLocal()
