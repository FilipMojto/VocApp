
import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from .. import models, schemas
from ..crud.models import word_crud
from .. import auth
from ..dbconfig import get_db

word_router = APIRouter(prefix="/words", tags=["words"])


@word_router.post("/", response_model=schemas.WordReturn)
async def create_word(
    word_create: schemas.WordCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    try:
        word = word_crud.create(
            obj_in=word_create,
            db=db,
        )
        

        return word

        # return schemas.WordReturn(**entry_create.model_dump(), id=entry_create.id)
    except IntegrityError as e:
        logging.error(e.orig)
        raise HTTPException(
            status_code=400,
            detail="Constraint violation: e.g. duplicate key or null field",
        )


@word_router.get("/{word_id}", response_model=schemas.WordReturn)
async def read_word(word_id: int, db: Session = Depends(get_db)):
    word = word_crud.get(id=word_id, db=db)

    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    return word


@word_router.get("/", response_model=list[schemas.WordReturn])
async def read_words(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return word_crud.get_multi(db=db, skip=skip, limit=limit)


@word_router.patch("/{word_id}", response_model=schemas.WordReturn)
async def update_word(
    word_id: int, word: schemas.WordUpdate, db: Session = Depends(get_db)
):
    # db_entry = word_crud.update(obj_in=entry, obj_id=word_id, db=db)

    # if db_entry is None:
    #     raise HTTPException(status_code=404, detail="Entry not found")

    # return db_entry

    db_word = word_crud.get(id=word_id, db=db)
    if db_word is None:
        raise HTTPException(status_code=404, detail="Word not found")
    
    return word_crud.update(db=db, db_obj=db_word, obj_in=word)


@word_router.delete("/{word_id}", response_model=schemas.WordReturn)
async def delete_word(word_id: int, db: Session = Depends(get_db)):
    word = word_crud.delete(id=word_id, db=db)

    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    return word