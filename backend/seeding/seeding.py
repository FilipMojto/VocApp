from sqlalchemy.exc import IntegrityError
from typing import Optional

from .loading import DataLoader
from .loaders.json import JSONLoader
from .. import schemas as vocap_schemas
from ..crud.models import user_crud, word_crud, word_relation_crud, user_word_crud
from .. import models
from sqlalchemy.orm import Session
from .. import vocap_db_types as vocapp_types

SUPPORTED_SEEDERS = ["json"]


def seed_data(seeder: str, db: Session):
    """
    Seed database using the loader 'seeder' (currently supports 'json').

    Expects loader.load_data() -> List[UserEntryMapper], where:
      UserEntryMapper.user : vocap_schemas.UserCreate
      UserEntryMapper.entries : List[WordMapper]
      WordMapper.entry : vocap_schemas.WordCreate
      WordMapper.translations : List[vocap_schemas.WordCreate]
    """
    if seeder not in SUPPORTED_SEEDERS:
        raise ValueError(
            f"Unsupported seeder format: {seeder}. Supported formats: {SUPPORTED_SEEDERS}"
        )

    # instantiate loader
    if seeder == "json":
        loader: DataLoader = JSONLoader()
    else:
        raise ValueError(f"Unsupported seeder format: {seeder}")

    mappers = loader.load_data()  # List[UserEntryMapper]

    if not isinstance(mappers, list):
        raise ValueError("Loader must return a list of UserEntryMapper objects")

    for user_mapper in mappers:
        user_schema: vocap_schemas.UserCreate = user_mapper.user

        # Create user (CRUD handles password hashing via field_transformers)
        try:
            user = user_crud.create(obj_in=user_schema, db=db)
        except IntegrityError:
            db.rollback()
            # user already exists -> fetch by username
            user = user_crud.get_by_col_value(
                col="username", value=user_schema.username, db=db
            )
            if user is None:
                # unexpected; re-raise
                raise

        # Per-user operations; commit each user so a failure doesn't abort whole seed
        try:
            for word_mapper in user_mapper.vocabulary:
                word_schema: vocap_schemas.WordCreate = word_mapper.lexeme
                # Attempt to find existing global word by (lexeme, language_code)
                existing_word: Optional[models.Word] = (
                    db.query(models.Word)
                    .filter(models.Word.lexeme == word_schema.lexeme)
                    .filter(models.Word.language_code == word_schema.language_code)
                    .first()
                )

                if existing_word:
                    word = existing_word
                else:
                    # create global word
                    try:
                        word = word_crud.create(obj_in=word_schema, db=db)
                        user_word_schema = vocap_schemas.UserWordCreate(user_id=user.id, word_id=word.id)
                        user_word = user_word_crud.create(obj_in=user_word_schema, db=db)
                    except IntegrityError:
                        db.rollback()
                        word = (
                            db.query(models.Word)
                            .filter(models.Word.lexeme == word_schema.lexeme)
                            .filter(
                                models.Word.language_code == word_schema.language_code
                            )
                            .first()
                        )
                        if not word:
                            raise

                # Handle mapped (related) words
                for translation_schema in word_mapper.translations:
                    # mapped_schema is vocap_schemas.WordCreate
                    existing_mapped: Optional[models.Word] = (
                        db.query(models.Word)
                        .filter(models.Word.lexeme == translation_schema.lexeme)
                        .filter(
                            models.Word.language_code == translation_schema.language_code
                        )
                        .first()
                    )

                    if existing_mapped:
                        mapped_word = existing_mapped
                    else:
                        try:
                            mapped_word = word_crud.create(obj_in=translation_schema, db=db)
                        except IntegrityError:
                            db.rollback()
                            mapped_word = (
                                db.query(models.Word)
                                .filter(models.Word.lexeme == translation_schema.lexeme)
                                .filter(
                                    models.Word.language_code
                                    == translation_schema.language_code
                                )
                                .first()
                            )
                            if not mapped_word:
                                raise

                    # create the relation (word -> mapped_word), relation_type defaults to "translation"
                    try:
                        word_relation_crud.create(
                            obj_in=vocap_schemas.WordRelationCreate(
                                user_id=user.id,
                                word_id=word.id,
                                related_word_id=mapped_word.id,
                                relation_type="translation",
                            ),
                            db=db,
                        )
                    except IntegrityError:
                        db.rollback()  # relation probably exists; ignore

            # commit after processing this user's words
            db.commit()

        except Exception:
            # rollback this user's partial changes and continue with next user (or re-raise)
            db.rollback()
            raise

    # final commit (in case something still open) and finish
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    print("Seeding finished.")
