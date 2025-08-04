
from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from database.dbconfig import SessionLocal
from .crud.models import *
from . import schemas


app = FastAPI()
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dependencys
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ─────────────────────────────────────────────
# SECTION: Endpoints 
# ─────────────────────────────────────────────

# === Users ===

@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return user_crud.create(db=db, obj_in=user)
    except IntegrityError as e:
        logging.error(e.orig)
        raise HTTPException(status_code=400, detail="Constraint violation: e.g. duplicate key or null field")
        
@app.get("/users/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_crud.get_multi(db=db, skip=skip, limit=limit)

@app.get("/users/{user_id}/entries", response_model=list[schemas.LexicalEntry])
async def read_user_entries(user_id: int, db: Session = Depends(get_db)):
    entries: List[schemas.LexicalEntry] = entry_crud.get_by_col_value(col="user_id", value=user_id, db=db, many=True)

    if not entries:
        raise HTTPException(status_code=404, detail=f"No entries found for user_id: {user_id}")
    
    return entries

@app.get("/users/{user_id}/translations", response_model=list[schemas.Translation])
async def read_user_translations(user_id: int, db: Session = Depends(get_db)):
    entries: List[schemas.LexicalEntry] = await read_user_entries(user_id=user_id, db=db)
    translations: List[schemas.Translation] = []

    for entry in entries:
        translations.extend(await get_translations_by_entry(entry_id=entry.id, db=db))

    return translations

@app.patch("/users/{user_id}", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)):
    db_user = user_crud.update(obj_in=schemas.UserUpdate(id=user_id, **user.model_dump()),
                               db=db)
   
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.delete(id=user_id, db=db)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# === Lexical Entries ===

@app.post("/entries", response_model=schemas.LexicalEntry)
async def create_entry(entry: schemas.LexicalEntryCreate, db: Session = Depends(get_db)):
    try:
        return entry_crud.create(obj_in=entry, db=db)
    except IntegrityError as e:
        logging.error(e.orig)
        raise HTTPException(status_code=400, detail="Constraint violation: e.g. duplicate key or null field")


@app.get("/entries", response_model=schemas.LexicalEntry)
async def read_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = entry_crud.get(id=entry_id, db=db)

    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return db_entry

@app.get("/entries/", response_model=list[schemas.LexicalEntry])
async def read_entries(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return entry_crud.get_multi(db=db, skip=skip, limit=limit)

@app.patch("/entries/{entry_id}", response_model=schemas.LexicalEntry)
async def update_entry(entry_id: int, entry: schemas.LexicalEntryBase, db: Session = Depends(get_db)):
    db_entry = entry_crud.update(obj_in=schemas.LexicalEntryUpdate(**entry.model_dump(), id=entry_id))

    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return db_entry

@app.delete("/entries/{entry_id}", response_model=schemas.LexicalEntry)
async def delete_entry(entry_id: int, db: Session = Depends(get_db)):
    db_entry = entry_crud.delete(id=entry_id, db=db)

    if db_entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return db_entry

# === Translation ===
@app.post("/translations/", response_model=schemas.Translation)
async def create_translation(translation: schemas.TranslationCreate, db: Session = Depends(get_db)):
    try:
        db_trans = translation_crud.create(obj_in=translation, db=db)
        return db_trans
    except IntegrityError as e:
        logging.error(e.orig)
        raise HTTPException(status_code=400, detail="Constraint violation: e.g. duplicate key or null field")


@app.get("/translations/{trans_id}", response_model=schemas.Translation)
async def read_translation(trans_id, db: Session = Depends(get_db)):
    db_trans = translation_crud.get(id=trans_id, db=db)

    if db_trans is None:
        raise HTTPException(status_code=404, detail="Translation not found.")
    
    return db_trans

@app.get("/translations/", response_model=list[schemas.Translation])
async def read_translations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return translation_crud.get_multi(db=db, skip=skip, limit=limit)

@app.patch("/translations/{trans_id}", response_model=schemas.Translation)
async def update_trans(trans_id: int, trans: schemas.Translation, db: Session = Depends(get_db)):
    db_trans = translation_crud.update(obj_in=schemas.TranslationUpdate(id=trans_id, **trans.model_dump()), db=db)

    if db_trans is None:
        raise HTTPException(status_code=404, detail="Translation not found.")
    
    return db_trans

@app.delete("/translations/{trans_id}", response_model=schemas.Translation)
async def delete_trans(trans_id: int, db: Session = Depends(get_db)):
    db_trans = translation_crud.delete(id=trans_id, db=db)

    if db_trans is None:
        raise HTTPException(status_code=404, detail=f"Translation not found with id={trans_id}")
    
    return db_trans

@app.post("/entry_translations/", response_model=schemas.EntryTranslation)
async def create_entry_trans(entry_trans: schemas.EntryTranslationCreate, db: Session = Depends(get_db)):
    try:
        db_entry_trans = entry_translation_crud.create(obj_in=entry_trans, db=db)
        return db_entry_trans
    except IntegrityError as e:
        logging.error(e.orig)
        raise HTTPException(status_code=400, detail="Constraint violation: e.g. duplicate key or null field")

@app.get("/entry_translations/{entry_id}", response_model=list[schemas.Translation])
async def get_translations_by_entry(entry_id: int, db: Session = Depends(get_db)):
    entry_trans_list = entry_translation_crud.get_by_col_value(col="entry_id", value=entry_id, db=db, many=True)

    if not entry_trans_list:
        raise HTTPException(status_code=404, detail=f"No entry-translations found for id={entry_id}")
    
    translations: List[Translation] = []

    for entry_trans in entry_trans_list:
        translations.append(translation_crud.get(id=entry_trans.translation_id, db=db))

    return translations

@app.get("/entry_translations/{translation_id}", response_model=list[schemas.LexicalEntry])
async def get_entries_by_trans(trans_id: int, db: Session = Depends(get_db)):
    entry_trans_list = entry_translation_crud.get_by_col_value(col="translation_id", value=trans_id, db=db, many=True)

    if not entry_trans_list:
        raise HTTPException(status_code=404, detail=f"No entry-translations found for id={trans_id}")
    
    entries: List[LexicalEntry] = []

    for entry_trans in entry_trans_list:
        entries.append(entry_crud.get(id=entry_trans.entry_id, db=db))

    return entries
