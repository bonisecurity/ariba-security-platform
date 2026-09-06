from fastapi import Depends, SecurityAPIRouter
from sqlalchemy.orm import Session
from ariba_manager.app.db.session import SessionLocal, engine
from ariba_manager.app.core.config import settings
from ariba_manager.app.models import Base


# Create database tables on startup
def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


get_db = lambda: db_generator()


def db_generator():
    """Dependency to get DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()