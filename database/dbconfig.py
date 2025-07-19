# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

# # SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # Use PostgreSQL/MySQL URI in production

# # engine = create_engine(
# #     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}  # Needed for SQLite
# # )
# # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Base = declarative_base()

# engine = None
# SessionLocal = None
# Base = declarative_base()

# def get_database_url(db_type="sqlite", user=None, password=None, host=None, port=None, dbname=None):
#     if db_type == "sqlite":
#         return "sqlite:///./test.db"
#     elif db_type == "postgresql":
#         return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
#     else:
#         raise ValueError(f"Unsupported database type: {db_type}")


def init_db(database_url: str):
    global engine, SessionLocal
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    engine = create_engine(database_url, connect_args=connect_args)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def get_engine(db_url: str):
#     return create_engine(db_url, connect_args={"check_same_thread": False} if db_url.startswith("sqlite") else {})

# def get_session_local(engine):
#     return sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

def get_database_url(db_type="sqlite", user=None, password=None, host=None, port=None, dbname=None):
    if db_type == "sqlite":
        return "sqlite:///./test.db"
    elif db_type == "postgresql":
        return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

def get_engine(db_url: str):
    connect_args = {"check_same_thread": False} if db_url.startswith("sqlite") else {}
    return create_engine(db_url, connect_args=connect_args)

def get_session_local(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)