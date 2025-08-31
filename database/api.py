from typing import List
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from database import models

from .dbconfig import SessionLocal
from .crud.models import *
from . import schemas, auth


app = FastAPI()
origins = [
    "http://localhost:5173",  # your React frontend
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for testing
    allow_credentials=True,
    allow_methods=["*"],  # important: allow POST, OPTIONS, etc.
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
user_router = APIRouter(prefix="/users", tags=["users"])


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


@user_router.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)
):
    logging.info(f"Login attempt for user: {form_data.username}")

    user = user_crud.get_by_col_value(db=db, col="username", value=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # try:
    #     return user_crud.create(db=db, obj_in=user)
    # except IntegrityError as e:
    #     logging.error(e.orig)
    #     raise HTTPException(status_code=400, detail="Constraint violation: e.g. duplicate key or null field")
    # user.model_dump() contains {'username': ..., 'password': ...}
    data = user.model_dump()
    raw_password = data.get("password", None)
    if not raw_password:
        raise HTTPException(status_code=400, detail="Password required")
    data["hashed_password"] = auth.get_password_hash(raw_password)

    # Create directly (bypass CRUD) or call CRUD with a dict-like object:
    try:
        db_obj = models.User(**data)  # make a DB object
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    except IntegrityError as e:
        db.rollback()
        logging.error(e.orig)
        raise HTTPException(status_code=400, detail="Constraint violation")


@user_router.get("/me", response_model=schemas.UserReturn)
async def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
    # return current_user
    return schemas.UserReturn(id=current_user.id, username=current_user.username)


@user_router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.get("/", response_model=list[schemas.User])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_crud.get_multi(db=db, skip=skip, limit=limit)


# @user_router.get("/{user_id}/entries", response_model=list[schemas.LexicalEntry])
# async def read_user_entries(user_id: int, db: Session = Depends(get_db)):
#     entries: List[schemas.LexicalEntry] = entry_crud.get_by_col_value(
#         col="user_id", value=user_id, db=db, many=True
#     )

#     if not entries:
#         raise HTTPException(
#             status_code=404, detail=f"No entries found for user_id: {user_id}"
#         )

#     return entries

# @user_router.get("/{user_id}/entries", response_model=list[schemas.LexicalEntry])
async def __read_user_entries(user_id: int, db: Session = Depends(get_db)):
    entries: List[schemas.LexicalEntry] = entry_crud.get_by_col_value(
        col="user_id", value=user_id, db=db, many=True
    )

    if not entries:
        raise HTTPException(
            status_code=404, detail=f"No entries found for user_id: {user_id}"
        )

    return entries

async def __read_user_translations(user_id: int, db: Session = Depends(get_db)):
    translations: List[schemas.Translation] = translation_crud.get_by_col_value(
        col="user_id", value=user_id, db=db, many=True
    )

    if not translations:
        raise HTTPException(
            status_code=404, detail=f"No translations found for user_id: {user_id}"
        )

    return translations


@user_router.get("/me/entries", response_model=list[schemas.LexicalEntry])
async def read_my_entries(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return await __read_user_entries(user_id=current_user.id, db=db)


@user_router.get("/{user_id}/translations", response_model=list[schemas.Translation])
async def read_user_translations(user_id: int, db: Session = Depends(get_db)):
    entries: List[schemas.LexicalEntry] = await __read_user_entries(
        user_id=user_id, db=db
    )
    translations: List[schemas.Translation] = []

    for entry in entries:
        translations.extend(await get_translations_by_entry(entry_id=entry.id, db=db))

    return translations


@user_router.patch("/{user_id}", response_model=schemas.User)
async def update_user(
    user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)
):
    db_user = user_crud.update(
        obj_in=schemas.UserUpdate(id=user_id, **user.model_dump()), db=db
    )

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.delete(id=user_id, db=db)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# === Lexical Entries ===


@app.post("/entries", response_model=schemas.LexicalEntry)
async def create_entry(
    entry: schemas.LexicalEntryCreate, db: Session = Depends(get_db)
):
    try:
        return entry_crud.create(obj_in=entry, db=db)
    except IntegrityError as e:
        logging.error(e.orig)
        raise HTTPException(
            status_code=400,
            detail="Constraint violation: e.g. duplicate key or null field",
        )


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
async def update_entry(
    entry_id: int, entry: schemas.LexicalEntryBase, db: Session = Depends(get_db)
):
    db_entry = entry_crud.update(
        obj_in=schemas.LexicalEntryUpdate(**entry.model_dump(), id=entry_id)
    )

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
async def create_translation(
    translation: schemas.TranslationBase, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)
):
    try:
        db_trans = translation_crud.create(obj_in=schemas.TranslationCreate(**translation.model_dump(), user_id=current_user.id), db=db)
        return db_trans
    except IntegrityError as e:
        logging.error(e.orig)
        raise HTTPException(
            status_code=400,
            detail="Constraint violation: e.g. duplicate key or null field",
        )


@app.get("/translations/{trans_id}", response_model=schemas.Translation)
async def read_translation(trans_id, db: Session = Depends(get_db)):
    db_trans = translation_crud.get(id=trans_id, db=db)

    if db_trans is None:
        raise HTTPException(status_code=404, detail="Translation not found.")

    return db_trans


@app.get("/translations/", response_model=list[schemas.Translation])
async def read_translations(
    skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return translation_crud.get_multi(db=db, skip=skip, limit=limit)


@app.patch("/translations/{trans_id}", response_model=schemas.Translation)
async def update_trans(
    trans_id: int, trans: schemas.Translation, db: Session = Depends(get_db)
):
    db_trans = translation_crud.update(
        obj_in=schemas.TranslationUpdate(id=trans_id, **trans.model_dump()), db=db
    )

    if db_trans is None:
        raise HTTPException(status_code=404, detail="Translation not found.")

    return db_trans


@app.delete("/translations/{trans_id}", response_model=schemas.Translation)
async def delete_trans(trans_id: int, db: Session = Depends(get_db)):
    db_trans = translation_crud.delete(id=trans_id, db=db)

    if db_trans is None:
        raise HTTPException(
            status_code=404, detail=f"Translation not found with id={trans_id}"
        )

    return db_trans


@app.post("/entry_translations/", response_model=schemas.EntryTranslation)
async def create_entry_trans(
    entry_trans: schemas.EntryTranslationBase, db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    try:
            # Ensure the current user owns both the entry and the translation
        user_entries = await __read_user_entries(user_id=current_user.id, db=db)
        user_translations = await __read_user_translations(user_id=current_user.id, db=db)

        if not any(entry.id == entry_trans.entry_id for entry in user_entries):
            raise HTTPException(status_code=403, detail="Not authorized to link this entry.")
        if not any(translation.id == entry_trans.translation_id for translation in user_translations):
            raise HTTPException(status_code=403, detail="Not authorized to link this translation.")
        
        db_entry_trans = entry_translation_crud.create(obj_in=schemas.EntryTranslationCreate(**entry_trans.model_dump()), db=db)
        return db_entry_trans
    except IntegrityError as e:
        logging.error(e.orig)
        raise HTTPException(
            status_code=400,
            detail="Constraint violation: e.g. duplicate key or null field",
        )


@app.get("/entry_translations/{entry_id}", response_model=list[schemas.Translation])
async def get_translations_by_entry(entry_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    user_entries = await __read_user_entries(user_id=current_user.id, db=db)
    
    if not user_entries:
        raise HTTPException(status_code=404, detail="No entries found for the current user.")

    if not any(entry.id == entry_id for entry in user_entries):
        raise HTTPException(status_code=403, detail="Not authorized to access this entry's translations.")
    
    
    entry_trans_list = entry_translation_crud.get_by_col_value(
        col="entry_id", value=entry_id, db=db, many=True
    )

    if not entry_trans_list:
        raise HTTPException(
            status_code=404, detail=f"No entry-translations found for id={entry_id}"
        )

    translations: List[Translation] = []

    for entry_trans in entry_trans_list:
        translations.append(translation_crud.get(id=entry_trans.translation_id, db=db))

    return translations


@app.get(
    "/entry_translations/{translation_id}", response_model=list[schemas.LexicalEntry]
)
async def get_entries_by_trans(trans_id: int, db: Session = Depends(get_db)):
    entry_trans_list = entry_translation_crud.get_by_col_value(
        col="translation_id", value=trans_id, db=db, many=True
    )

    if not entry_trans_list:
        raise HTTPException(
            status_code=404, detail=f"No entry-translations found for id={trans_id}"
        )

    entries: List[LexicalEntry] = []

    for entry_trans in entry_trans_list:
        entries.append(entry_crud.get(id=entry_trans.entry_id, db=db))

    return entries


app.include_router(user_router)
