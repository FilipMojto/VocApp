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
from .routers import users, words, user_words, word_relations

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

# user_router = APIRouter(prefix="/users", tags=["users"])
# word_router = APIRouter(prefix="/words", tags=["words"])
# user_word_router = APIRouter(prefix="/userwords", tags=["userwords"])
# word_relation_router = APIRouter(prefix="/wordrelations", tags=["wordrelations"])


# # Dependencys
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# ─────────────────────────────────────────────
# SECTION: Endpoints
# ─────────────────────────────────────────────

# === Users ===


# @user_router.post("/auth/login")
# def login(
#     form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)
# ):
#     logging.info(f"Login attempt for user: {form_data.username}")

#     user = user_crud.get_by_col_value(db=db, col="username", value=form_data.username)
#     if not user or not auth.verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
#         )

#     access_token = auth.create_access_token(data={"sub": str(user.id)})
#     return {"access_token": access_token, "token_type": "bearer"}


# @user_router.post("/", response_model=schemas.UserReturn)
# async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     data = user.model_dump()
#     raw_password = data.get("password", None)
#     if not raw_password:
#         raise HTTPException(status_code=400, detail="Password required")
#     data["hashed_password"] = auth.get_password_hash(raw_password)

#     # Create directly (bypass CRUD) or call CRUD with a dict-like object:
#     try:
#         db_obj = models.User(**data)  # make a DB object
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj
#     except IntegrityError as e:
#         db.rollback()
#         logging.error(e.orig)
#         raise HTTPException(status_code=400, detail="Constraint violation")


# @user_router.get("/me", response_model=schemas.UserReturn)
# async def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
#     return schemas.UserReturn(id=current_user.id, username=current_user.username)


# @user_router.get("/{user_id}", response_model=schemas.UserBase)
# async def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = user_crud.get(db=db, id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @user_router.get("/", response_model=list[schemas.UserBase])
# async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return user_crud.get_multi(db=db, skip=skip, limit=limit)


# async def __read_user_words(user_id: int, db: Session = Depends(get_db)):
#     entries: List[schemas.WordReturn] = word_crud.get_by_col_value(
#         col="user_id", value=user_id, db=db, many=True
#     )
    

#     if not entries:
#         raise HTTPException(
#             status_code=404, detail=f"No entries found for user_id: {user_id}"
#         )

#     return entries


# @user_router.get("/me/words", response_model=list[schemas.WordReturn])
# async def read_my_words(
#     current_user: models.User = Depends(auth.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     return await __read_user_words(user_id=current_user.id, db=db)


# @user_router.patch("/{user_id}", response_model=schemas.UserBase)
# async def update_user(
#     user_id: int, user: schemas.UserBase, db: Session = Depends(get_db)
# ):
#     db_user = user_crud.get(id=user_id, db=db)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
    
#     return user_crud.update(db=db, db_obj=db_user, obj_in=user)
#     # db_user = user_crud.update(
#     #     # obj_in=schemas.UserUpdate(id=user_id, **user.model_dump()), db=db
        
#     # )

#     # if db_user is None:
#     #     raise HTTPException(status_code=404, detail="User not found")
#     # return db_user


# @user_router.delete("/{user_id}", response_model=schemas.UserBase)
# async def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = user_crud.delete(id=user_id, db=db)

#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# === Lexical Entries ===


# @word_router.post("/", response_model=schemas.WordReturn)
# async def create_word(
#     word_create: schemas.WordCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(auth.get_current_user),
# ):
#     try:
#         word = word_crud.create(
#             obj_in=word_create,
#             db=db,
#         )

#         return word

#         # return schemas.WordReturn(**entry_create.model_dump(), id=entry_create.id)
#     except IntegrityError as e:
#         logging.error(e.orig)
#         raise HTTPException(
#             status_code=400,
#             detail="Constraint violation: e.g. duplicate key or null field",
#         )


# @word_router.get("/{entry_id}", response_model=schemas.WordReturn)
# async def read_word(entry_id: int, db: Session = Depends(get_db)):
#     word = word_crud.get(id=entry_id, db=db)

#     if word is None:
#         raise HTTPException(status_code=404, detail="Entry not found")

#     return word


# @word_router.get("/", response_model=list[schemas.WordReturn])
# async def read_words(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return word_crud.get_multi(db=db, skip=skip, limit=limit)


# @word_router.patch("/{entry_id}", response_model=schemas.WordReturn)
# async def update_word(
#     word_id: int, word: schemas.WordUpdate, db: Session = Depends(get_db)
# ):
#     # db_entry = word_crud.update(obj_in=entry, obj_id=word_id, db=db)

#     # if db_entry is None:
#     #     raise HTTPException(status_code=404, detail="Entry not found")

#     # return db_entry

#     db_word = word_crud.get(id=word_id, db=db)
#     if db_word is None:
#         raise HTTPException(status_code=404, detail="Entry not found")
    
#     return word_crud.update(db=db, db_obj=db_word, obj_in=word)


# @word_router.delete("/{entry_id}", response_model=schemas.WordReturn)
# async def delete_entry(entry_id: int, db: Session = Depends(get_db)):
#     db_entry = word_crud.delete(id=entry_id, db=db)

#     if db_entry is None:
#         raise HTTPException(status_code=404, detail="Entry not found")

#     return db_entry

# === UserWord ===

# @user_word_router.post("/", response_model=schemas.UserWordBase)
# async def create_user_word(
#     user_word: schemas.UserWordCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(auth.get_current_user),
# ):
#     try:
#         db_user_word = user_relation_crud.create(
#             obj_in=user_word,
#             db=db,
#         )
#         return db_user_word
#     except IntegrityError as e:
#         logging.error(e.orig)
#         raise HTTPException(
#             status_code=400,
#             detail="Constraint violation: e.g. duplicate key or null field",
#         )
    
# @user_word_router.get("/{user_word_id}", response_model=schemas.UserWordBase)
# async def read_user_word(user_word_id: int, db: Session = Depends(get_db)):
#     db_user_word = user_relation_crud.get(id=user_word_id, db=db)

#     if db_user_word is None:
#         raise HTTPException(status_code=404, detail="UserWord not found")

#     return db_user_word

# @user_word_router.get("/", response_model=list[schemas.UserWordBase])
# async def read_user_words(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return user_relation_crud.get_multi(db=db, skip=skip, limit=limit)

# @user_word_router.patch("/{user_word_id}", response_model=schemas.UserWordBase)
# async def update_user_word(
#     user_word_id: int, user_word: schemas.UserWordUpdate, db: Session = Depends(get_db)
# ):
#     # db_user_word = user_relation_crud.update(
#     #     obj_in=user_word, obj_id=user_word_id, db=db
#     # )

#     # if db_user_word is None:
#     #     raise HTTPException(status_code=404, detail="UserWord not found")

#     # return db_user_word

#     db_user_word = user_relation_crud.get(id=user_word_id, db=db)
#     if db_user_word is None:
#         raise HTTPException(status_code=404, detail="UserWord not found")
    
#     return user_relation_crud.update(db=db, db_obj=db_user_word, obj_in=user_word)

# @user_word_router.delete("/{user_word_id}", response_model=schemas.UserWordBase)
# async def delete_user_word(user_word_id: int, db: Session = Depends(get_db)):
#     db_user_word = user_relation_crud.delete(id=user_word_id, db=db)

#     if db_user_word is None:
#         raise HTTPException(status_code=404, detail="UserWord not found")

#     return db_user_word


# === WordRelation ===

# @word_relation_router.post("/", response_model=schemas.WordRelationReturn)
# async def create_word_relation(
#     word_relation: schemas.WordRelationCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(auth.get_current_user),
# ):
#     try:
#         db_word_relation = word_relation_crud.create(
#             obj_in=word_relation,
#             db=db,
#         )
#         return db_word_relation
#     except IntegrityError as e:
#         logging.error(e.orig)
#         raise HTTPException(
#             status_code=400,
#             detail="Constraint violation: e.g. duplicate key or null field",
#         )
    
# @word_relation_router.get("/{word_relation_id}", response_model=schemas.WordRelationReturn)
# async def read_word_relation(word_relation_id: int, db: Session = Depends(get_db)):
#     db_word_relation = word_relation_crud.get(id=word_relation_id, db=db)

#     if db_word_relation is None:
#         raise HTTPException(status_code=404, detail="WordRelation not found")

#     return db_word_relation

# @word_relation_router.get("/", response_model=list[schemas.WordRelationReturn])
# async def read_word_relations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return word_relation_crud.get_multi(db=db, skip=skip, limit=limit)

# @word_relation_router.patch("/{word_relation_id}", response_model=schemas.WordRelationReturn)
# async def update_word_relation(
#     word_relation_id: int, word_relation: schemas.WordRelationUpdate, db: Session = Depends(get_db)
# ):
#     # db_word_relation = word_relation_crud.update(
#     #     obj_in=word_relation, obj_id=word_relation_id, db=db
#     # )

#     # if db_word_relation is None:
#     #     raise HTTPException(status_code=404, detail="WordRelation not found")

#     # return db_word_relation

#     db_word_relation = word_relation_crud.get(id=word_relation_id, db=db)
#     if db_word_relation is None:
#         raise HTTPException(status_code=404, detail="WordRelation not found")
    
#     return word_relation_crud.update(db=db, db_obj=db_word_relation, obj_in=word_relation)

# @word_relation_router.delete("/{word_relation_id}", response_model=schemas.WordRelationReturn)
# async def delete_word_relation(word_relation_id: int, db: Session = Depends(get_db)):
#     db_word_relation = word_relation_crud.delete(id=word_relation_id, db=db)

#     if db_word_relation is None:
#         raise HTTPException(status_code=404, detail="WordRelation not found")

#     return db_word_relation

app.include_router(users.user_router)
app.include_router(words.word_router)
app.include_router(user_words.user_word_router)
app.include_router(word_relations.word_relation_router)

