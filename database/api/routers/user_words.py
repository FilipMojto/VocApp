from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ... import models, schemas
from ...crud.models import user_relation_crud
from ... import auth
from ...dbconfig import get_db
from ..utils import handle_integrity_error


user_word_router = APIRouter(prefix="/userwords", tags=["userwords"])


@user_word_router.post("/", response_model=schemas.UserWordBase)
async def create_user_word(
    user_word: schemas.UserWordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    try:
        db_user_word = user_relation_crud.create(
            obj_in=user_word,
            db=db,
        )
        return db_user_word
    except IntegrityError as e:
        handle_integrity_error(e)
    

@user_word_router.get("/{user_word_id}", response_model=schemas.UserWordBase)
async def read_user_word(user_word_id: int, db: Session = Depends(get_db)):
    db_user_word = user_relation_crud.get(id=user_word_id, db=db)

    if db_user_word is None:
        raise HTTPException(status_code=404, detail="UserWord not found")

    return db_user_word


@user_word_router.get("/", response_model=list[schemas.UserWordBase])
async def read_user_words(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return user_relation_crud.get_multi(db=db, skip=skip, limit=limit)


@user_word_router.patch("/{user_word_id}", response_model=schemas.UserWordBase)
async def update_user_word(
    user_word_id: int, user_word: schemas.UserWordUpdate, db: Session = Depends(get_db)
):
    db_user_word = user_relation_crud.get(id=user_word_id, db=db)
    if db_user_word is None:
        raise HTTPException(status_code=404, detail="UserWord not found")
    
    return user_relation_crud.update(db=db, db_obj=db_user_word, obj_in=user_word)


@user_word_router.delete("/{user_word_id}", response_model=schemas.UserWordBase)
async def delete_user_word(user_word_id: int, db: Session = Depends(get_db)):
    db_user_word = user_relation_crud.delete(id=user_word_id, db=db)

    if db_user_word is None:
        raise HTTPException(status_code=404, detail="UserWord not found")

    return db_user_word