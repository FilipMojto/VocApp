
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session


from ... import models, schemas
from ...crud.models import user_crud, word_crud

from ... import auth
from ...dbconfig import get_db
from ..utils import handle_integrity_error

user_router = APIRouter(prefix="/users", tags=["users"])

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


@user_router.post("/", response_model=schemas.UserReturn)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    data = user.model_dump()
    raw_password = data.get("password", None)
    if not raw_password:
        raise HTTPException(status_code=400, detail="Password required")
    
    data["hashed_password"] = auth.get_password_hash(raw_password)

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
    entries: List[schemas.WordReturn] = word_crud.get_by_col_value(
        col="user_id", value=user_id, db=db, many=True
    )

    if not entries:
        raise HTTPException(
            status_code=404, detail=f"No entries found for user_id: {user_id}"
        )

    return entries


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
