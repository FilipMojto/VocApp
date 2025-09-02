

import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .. import models, schemas
from ..crud.models import word_relation_crud
from .. import auth
from ..dbconfig import get_db

word_relation_router = APIRouter(prefix="/wordrelations", tags=["wordrelations"])

@word_relation_router.post("/", response_model=schemas.WordRelationReturn)
async def create_word_relation(
    word_relation: schemas.WordRelationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    try:
        word_relation = word_relation_crud.create(
            obj_in=word_relation,
            db=db,
        )
        
        return word_relation
    except IntegrityError as e:
        logging.error(e.orig)
        raise HTTPException(
            status_code=400,
            detail="Constraint violation: e.g. duplicate key or null field",
        )


@word_relation_router.get("/{word_relation_id}", response_model=schemas.WordRelationReturn)
async def read_word_relation(word_relation_id: int, db: Session = Depends(get_db)):
    db_word_relation = word_relation_crud.get(id=word_relation_id, db=db)

    if db_word_relation is None:
        raise HTTPException(status_code=404, detail="WordRelation not found")

    return db_word_relation


@word_relation_router.get("/", response_model=list[schemas.WordRelationReturn])
async def read_word_relations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return word_relation_crud.get_multi(db=db, skip=skip, limit=limit)


@word_relation_router.patch("/{word_relation_id}", response_model=schemas.WordRelationReturn)
async def update_word_relation(
    word_relation_id: int, word_relation: schemas.WordRelationUpdate, db: Session = Depends(get_db)
):
    db_word_relation = word_relation_crud.get(id=word_relation_id, db=db)
    if db_word_relation is None:
        raise HTTPException(status_code=404, detail="WordRelation not found")
    
    return word_relation_crud.update(db=db, db_obj=db_word_relation, obj_in=word_relation)


@word_relation_router.delete("/{word_relation_id}", response_model=schemas.WordRelationReturn)
async def delete_word_relation(word_relation_id: int, db: Session = Depends(get_db)):
    db_word_relation = word_relation_crud.delete(id=word_relation_id, db=db)

    if db_word_relation is None:
        raise HTTPException(status_code=404, detail="WordRelation not found")

    return db_word_relation