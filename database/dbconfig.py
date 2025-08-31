from typing import Literal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def init_db(database_url: str):
    global engine, SessionLocal
    connect_args = (
        {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    )
    engine = create_engine(database_url, connect_args=connect_args)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()

type Database = Literal["dd"]


def get_database_url(
    db_type: Database,
    dbname: str,
    user: str = None,
    password: str = None,
    host: str = None,
    port: str = None,
):
    if db_type == "sqlite":
        return f"sqlite:///./{dbname}.db"
    elif db_type == "postgresql":
        return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")


def get_engine(db_url: str):
    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    return create_engine(db_url, connect_args=connect_args)


def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)
