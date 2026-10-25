import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.app.config import settings

# Ensure data directory exists
os.makedirs(os.path.dirname(settings.DATABASE_URL.replace("sqlite:///", "")), exist_ok=True)

# Main engine for administrative tasks & seeding
connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_readonly_engine():
    """
    Returns an engine configured strictly for read-only access.
    For SQLite: uses uri=True and mode=ro.
    For PostgreSQL: sets transaction read only.
    """
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite:///"):
        # Extract filepath and make URI read-only
        db_path = db_url.replace("sqlite:///", "")
        abs_path = os.path.abspath(db_path)
        ro_url = f"sqlite:///file:{abs_path}?mode=ro&uri=true"
        return create_engine(ro_url, connect_args={"check_same_thread": False}, pool_pre_ping=True)
    else:
        # Standard postgres or other engine
        return create_engine(db_url, pool_pre_ping=True, execution_options={"isolation_level": "AUTOCOMMIT"})
