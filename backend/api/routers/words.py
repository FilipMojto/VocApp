import logging
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from ... import models, schemas
from ...crud.models import word_crud, user_word_crud, word_relation_crud
from ... import auth
from ...dbconfig import get_db
from ..utils import handle_integrity_error

word_router = APIRouter(prefix="/words", tags=["words"])

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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

        user_word = user_word_crud.create(
            obj_in=schemas.UserWordCreate(user_id=current_user.id, word_id=word.id),
            db=db,
        )

        return word
    except IntegrityError as e:
        handle_integrity_error(e)


@word_router.get("/{word_id}", response_model=schemas.WordReturn)
async def read_word(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # word = word_crud.get(id=word_id, db=db)
    word = word_crud.get_by_col_value(
        db=db, col={"id": word_id, "user_id": current_user.id}, use_or=False, many=False
    )

    if word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    return word


@word_router.get("/", response_model=list[schemas.WordReturn])
async def read_words(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return word_crud.get_multi(db=db, skip=skip, limit=limit)


@word_router.get("/translations", response_model=list[schemas.WordReturn])
async def read_translations(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    word = word_crud.get_by_col_value(col="id", value=word_id, db=db, many=False)

    if not word:
        raise HTTPException(status_code=404, detail="Word not found")

    translations = (
        db.query(models.Word)
        .join(
            models.WordRelation, models.Word.id == models.WordRelation.related_word_id
        )
        .filter(models.WordRelation.word_id == word_id)
        .union(
            db.query(models.Word)
            .join(models.WordRelation, models.Word.id == models.WordRelation.word_id)
            .filter(models.WordRelation.related_word_id == word_id)
        )
        .all()
    )

    return translations


@word_router.patch("/{word_id}", response_model=schemas.WordReturn)
async def update_word(
    word_id: int,
    word: schemas.WordUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # db_word = word_crud.get(id=word_id, db=db)
    db_word = word_crud.filter(col="id", value=word_id, db=db, many=False)

    if db_word is None:
        raise HTTPException(status_code=404, detail="Word not found")

    return word_crud.update(db=db, db_obj=db_word, obj_in=word)


@word_router.delete("/{word_id}", response_model=schemas.WordReturn)
async def delete_word(
    word_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    PREFIX_LABEL = 'words - delete_word'

    # with db.begin():
    user_word = user_word_crud.filter(
        col={
            "user_id__ne": current_user.id,
            "word_id": word_id
        },
        db=db,
        many=False
    )

    if user_word is not None:
        logging.info(f"{PREFIX_LABEL}: Another user created the word. Skipping...")
    else:
        logging.info(f"{PREFIX_LABEL}: No other user created the word. Proceeding...")

        word_relation = word_relation_crud.filter(
            col={
                "related_word_id": word_id
            },
            db=db,
            many=False
        )

        if word_relation is not None:
            logging.info(f"{PREFIX_LABEL}: The word is mapped as a relation. Skipping...")
        else:
            logging.info(f"{PREFIX_LABEL}: The word is not mapped as a relation. Proceeding...")

            word = word_crud.delete(id=word_id, db=db, commit=False)

            if word is None:
                raise HTTPException(status_code=404, detail="Word not found")
            
            db.commit()
            logging.info(f"{PREFIX_LABEL}: Operation executed - deleted word with id {word_id}.")
            return word

    db.rollback()
    logging.info(f"{PREFIX_LABEL}: Operation not executed - failed to fulfill one or more conditions.")
    return Response(status_code=204)
