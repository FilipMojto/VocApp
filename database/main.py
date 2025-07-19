import uvicorn
import argparse
import sys
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .crud import crud
# print("name", __name__)
# print("package", __package__)
# print("sys", sys.path)

from . import schemas
from .dbconfig import Base, get_engine, get_session_local, init_db, get_database_url
from .seeding import seed_data
from .crud import crud as vocap_crud
from . import schemas as vocap_schemas
from .models import *

app = FastAPI()

print("name", __name__)
print("package", __package__)

user_crud = vocap_crud.CRUDBase[User, vocap_schemas.UserCreate](User)
entry_crud = vocap_crud.CRUDBase[LexicalEntry, vocap_schemas.LexicalEntryCreate](LexicalEntry)
translation_crud = vocap_crud.CRUDBase[Translation, vocap_schemas.TranslationCreate](Translation)
entry_translation_crud = vocap_crud.CRUDBase[EntryTranslation, vocap_schemas.EntryTranslationCreate](EntryTranslation)


# Dependencys
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_crud.create(db, user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_crud.get_multi(db, skip=skip, limit=limit)

def parse_args():
    parser = argparse.ArgumentParser(description="Launch FastAPI with custom DB config")
    parser.add_argument("--db_type", choices=["sqlite", "postgresql"], default="sqlite")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default="5432")
    parser.add_argument("--user", default="postgres")
    parser.add_argument("--password", default="postgres")
    parser.add_argument("--dbname", default="testdb")
    parser.add_argument("--api_host", default="127.0.0.1")
    parser.add_argument("--api_port", default=8000, type=int)

    parser.add_argument("--seed", default=None, type=str, required=False)
    return parser.parse_args()

args = parse_args()

db_url = get_database_url(
    db_type=args.db_type,
    user=args.user,
    password=args.password,
    host=args.host,
    port=args.port,
    dbname=args.dbname
)

engine = get_engine(db_url)
SessionLocal = get_session_local(engine)
init_db(db_url)
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    # args = parse_args()

    # db_url = get_database_url(
    #     db_type=args.db_type,
    #     user=args.user,
    #     password=args.password,
    #     host=args.host,
    #     port=args.port,
    #     dbname=args.dbname
    # )

    # engine = get_engine(db_url)


    # init_db(db_url)
    # Base.metadata.create_all(bind=engine)
    if args.seed:
        seed_data(seeder=args.seed, conn=None, db=SessionLocal())
    uvicorn.run("database.main:app", host=args.api_host, port=args.api_port, reload=True)