
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from ... import models, schemas
from ...crud.models import user_crud, user_word_crud

from ... import auth
from ... import security
from ...dbconfig import get_db
from ..utils import handle_integrity_error

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/auth/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(auth.get_db)
):
    logging.info(f"Login attempt for user: {form_data.username}")

    user = user_crud.filter(db=db, col="username", value=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@user_router.post("/", response_model=schemas.UserReturn)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    data = user.model_dump()
    raw_password = data.get("password", None)
    if not raw_password:
        raise HTTPException(status_code=400, detail="Password required")
    
    data["hashed_password"] = security.get_password_hash(raw_password)

    # Create directly (bypass CRUD) or call CRUD with a dict-like object:
    try:
        user_obj = user_crud.create(obj_in=user, db=db)
        return user_obj
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)


@user_router.get("/me", response_model=schemas.UserReturn)
async def read_current_user(current_user: models.User = Depends(auth.get_current_user)):
    return schemas.UserReturn(id=current_user.id, username=current_user.username)


@user_router.get("/{user_id}", response_model=schemas.UserReturn)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.get(db=db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.get("/", response_model=list[schemas.UserReturn])
async def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_crud.get_multi(db=db, skip=skip, limit=limit)


async def __read_user_words(user_id: int, db: Session = Depends(get_db)):
    user_words = user_word_crud.filter(
        col="user_id", value=user_id, db=db, many=True
    )

    if not user_words:
        return []

    # gather ids from join table
    word_ids = [uw.word_id for uw in user_words]
    print("1", word_ids)
    # one query to load all words
    words = db.query(models.Word).filter(models.Word.id.in_(word_ids)).all()
    print([w.id for w in words])
    # keep the original ordering of user_words (optional)
    id_to_word = {w.id: w for w in words}
    print(id_to_word)
    ordered_words = [id_to_word[w_id] for w_id in word_ids if w_id in id_to_word]

    # debug
    for w in ordered_words:
        print("loaded word id:", w.id)

    return ordered_words


@user_router.get("/me/words", response_model=list[schemas.WordReturn])
async def read_my_words(
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    return await __read_user_words(user_id=current_user.id, db=db)


@user_router.patch("/{user_id}", response_model=schemas.UserReturn)
async def update_user(
    user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)
):
    db_user = user_crud.get(id=user_id, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_crud.update(db=db, db_obj=db_user, obj_in=user)


@user_router.delete("/{user_id}", response_model=schemas.UserReturn)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = user_crud.delete(id=user_id, db=db)

    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
