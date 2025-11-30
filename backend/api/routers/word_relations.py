import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ... import models, schemas
from ...crud.models import word_relation_crud, word_crud, user_word_crud
from ... import auth
from ...dbconfig import get_db
from ..utils import handle_integrity_error
from ... import vocap_db_types as dbtypes

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

word_relation_router = APIRouter(prefix="/wordrelations", tags=["wordrelations"])

@word_relation_router.post("/", response_model=schemas.WordRelationReturn)
async def create_word_relation(
    word_id: int,
    translation_create: schemas.WordCreate,
    relation_type: dbtypes.WordRelationType,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    # with db.begin():
    try:
        word = word_crud.filter(col="id", value=word_id, many=False, db=db)

        if not word:
            raise HTTPException(
                detail=f"Translation Creation Failed - Word with {word_id} not found!"
            )

        try:
            translation = word_crud.create(obj_in=translation_create, db=db,
                                            commit=False)
        except IntegrityError:
            # Translation already exists, fetching it instead...
            translation = word_crud.filter(
                col="lexeme", value=translation_create.lexeme, many=False, db=db
            )

        try:
            user_word = user_word_crud.create(
                obj_in=schemas.UserWordCreate(
                    user_id=current_user.id,
                    word_id=translation.id,
                ),
                db=db,
                commit=False
            )
        except IntegrityError:
            # User has created the word already, skipping this step...
            ...

        word_relation = word_relation_crud.create(
            obj_in=schemas.WordRelationCreate(
                user_id=current_user.id,
                word_id=word.id,
                related_word_id=translation.id,
                relation_type=relation_type,
            ),
            commit=False,
            db=db,
        )

        db.commit()
        return word_relation
    except IntegrityError as e:
        db.rollback()
        handle_integrity_error(e)


# async def delete_word_relation(
#     word_relation_create: schemas.WordRelationCreate,
#     db: Session = Depends(get_db),
#     current_user: models.User = Depends(auth.get_current_user),
# ):
#     try:
#         word_relation_crud.delete(
#             db=db,
#             user_id=current_user.id,
#             word_id=word_relation_create.word_id,
#             related_word_id=word_relation_create.related_word_id,
#             relation_type=word_relation_create.relation_type,
#         )

#         user_word_crud.delete(
#             db=db, user_id=current_user.id, word_id=word_relation_create.related_word_id
#         )

#     except IntegrityError as e:
#         handle_integrity_error(e)


@word_relation_router.get(
    "/{word_id}", response_model=List[schemas.RelationEntryReturn]
)
async def read_word_entries(
    word_id: int,
    relation_type: dbtypes.WordRelationType = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):

    filters = {"user_id": current_user.id, "word_id": word_id}

    if relation_type is not None:
        filters["relation_type"] = relation_type

    word_relations = word_relation_crud.filter(
        col=filters,
        db=db,
        many=True,
        use_or=False,
    )

    if not word_relations:
        raise HTTPException(status_code=404, detail="WordRelation not found")

    relation_entries: List[schemas.RelationEntryReturn] = []

    for relation in word_relations:
        word = word_crud.filter(
            col="id",
            value=relation.related_word_id,
            many=False,
            use_or=False,
            db=db,
        )

        word_dict = schemas.WordReturn.model_validate(word.__dict__).model_dump()
        relation_dict = schemas.WordRelationReturn.model_validate(
            relation.__dict__
        ).model_dump()

        relation_entries.append(
            schemas.RelationEntryReturn(**word_dict, **relation_dict)
        )

    return relation_entries


@word_relation_router.patch(
    "/{word_relation_id}", response_model=schemas.WordRelationReturn
)
async def update_word_relation(
    word_relation_id: int,
    word_relation: schemas.WordRelationUpdate,
    db: Session = Depends(get_db),
):
    with db.begin():
        db_word_relation = word_relation_crud.filter(
            col="related_word_id", value=word_relation_id, db=db
        )
        if db_word_relation is None:
            raise HTTPException(status_code=404, detail="WordRelation not found")

        return word_relation_crud.update(
            db=db, db_obj=db_word_relation, obj_in=word_relation, commit=True
        )


@word_relation_router.delete(
    "/", response_model=schemas.WordRelationReturn
)
async def delete_word_relation(
    relation_entry: schemas.RelationEntryBase, db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    # with db.begin():
        
    # db_word_relation = word_relation_crud.delete(id=word_relation_id, db=db)
    db_word_relation = word_relation_crud.delete(
        user_id=relation_entry.user_id,
        word_id=relation_entry.word_id,
        related_word_id=relation_entry.related_word_id,
        relation_type=relation_entry.relation_type,
        db=db,
        commit=False,
    )

    if db_word_relation is None:
        raise HTTPException(status_code=404, detail="WordRelation not found")

    # now we are going to check whether we can safely remove the translation
    # it happens only if:
    # - there are no records of it in users_words (another user created it)
    # - there are also no records in of it in words_relations (another user
    #   used it as a relation)
    user_word = user_word_crud.filter(
        col={
            "word_id": relation_entry.related_word_id,
            "user_id__ne": current_user.id,
            # "user_id": relation_entry.user_id,
        },
        db=db,
        many=False,
        use_or=False,
    )

    if user_word is None:
        logging.info("The word was not created by another user, we proceed to second condition")
        # The word was not created by any user, we proceed to second condition

        # word_relation = word_relation_crud.filter(
        #     col="related_word_id",
        #     value=relation_entry.related_word_id,
        #     many=False,
        #     db=db,
        # )
        word_relation = word_relation_crud.filter(
            col={
                "word_id__ne": relation_entry.word_id,
                "related_word_id": relation_entry.related_word_id
            },
            db=db,
            many=False
        )

        if word_relation is None:
            # now we can safely delete the relation from database completely
            word_crud.delete(id=relation_entry.related_word_id, db=db, commit=False)
        
            logging.info("The word was not used as a relation by another user, we delete it")

            db.commit()
            return db_word_relation
    else:
        logging.info("The word was created by another user, skipping...")

    logging.info("The word was used as a relation by another user, skipping...")
    db.rollback()
    return Response(status_code=204)
