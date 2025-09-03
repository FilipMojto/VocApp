# from sqlalchemy.orm import Session

# from .loaders.base import SeederInterface
# from .loaders.json import JSONLoader
# from . import schemas as vocap_schemas
# from .crud.models import *

# DB_PATH = "./vocapp.db"
# SUPPORTED_SEEDERS = ["json"]


# def seed_data(seeder: str, db: Session):
#     print("Seeding data...")
#     """Seed the database with initial data."""
#     if seeder not in SUPPORTED_SEEDERS:
#         raise ValueError(
#             f"Unsupported seeder format: {seeder}. Supported formats: {SUPPORTED_SEEDERS}"
#         )

#     module_instance: SeederInterface = None

#     match seeder:
#         case "json":
#             module_instance = JSONLoader()
#         case _:
#             raise ValueError(
#                 f"Unsupported seeder format: {seeder}. Supported formats: {SUPPORTED_SEEDERS}"
#             )

#     seed_data = module_instance.load_data()
#     print("seed:\n", seed_data)

#     # Insert users into the database
#     for user_entry_obj in seed_data:
#         user = user_crud.create(
#             db=db, obj_in=vocap_schemas.UserCreate(**user_entry_obj.user.model_dump())
#         )

#         for entry_trans_obj in user_entry_obj.entries:
#             entry = word_crud.create(
#                 db=db,
#                 obj_in=vocap_schemas.WordCreate(
#                     **entry_trans_obj.entry.model_dump()
#                 ),
#             )

#             for translation_obj in entry_trans_obj.translations:
#                 # Check if translation already exists
#                 existing = translation_crud.get_by_lexeme(
#                     db=db, lexeme=translation_obj.lexeme
#                 )

#                 if existing:
#                     translation = existing
#                 else:
#                     translation = translation_crud.create(
#                         db=db,
#                         obj_in=vocap_schemas.TranslationCreate(
#                             **translation_obj.model_dump()
#                         ),
#                     )

#                 # translation = translation_crud.create(db=db, obj_in=vocap_schemas.TranslationCreate(**translation_obj.model_dump()))
#                 word_relation_crud.create(
#                     db=db,
#                     obj_in=vocap_schemas.WordRelationCreate(
#                         entry_id=entry.id, translation_id=translation.id
#                     ),
#                 )

#     db.commit()


from sqlalchemy.exc import IntegrityError
from typing import Optional

from .loaders.base import SeederInterface
from .loaders.json import JSONLoader
from . import schemas as vocap_schemas
from .crud.models import user_crud, word_crud, user_relation_crud, word_relation_crud
from . import models
# from . import auth  # optional: for password hashing if available
from sqlalchemy.orm import Session

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
        raise ValueError(f"Unsupported seeder format: {seeder}. Supported formats: {SUPPORTED_SEEDERS}")

    # instantiate loader
    if seeder == "json":
        loader: SeederInterface = JSONLoader()
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
            user = user_crud.get_by_col_value(col="username", value=user_schema.username, db=db)
            if user is None:
                # unexpected; re-raise
                raise

        # Per-user operations; commit each user so a failure doesn't abort whole seed
        try:
            for word_mapper in user_mapper.entries:
                entry_schema: vocap_schemas.WordCreate = word_mapper.entry

                # Attempt to find existing global word by (lexeme, language_code)
                existing_word: Optional[models.Word] = (
                    db.query(models.Word)
                    .filter(models.Word.lexeme == entry_schema.lexeme)
                    .filter(models.Word.language_code == entry_schema.language_code)
                    .first()
                )

                if existing_word:
                    word = existing_word
                else:
                    # create global word
                    try:
                        word = word_crud.create(obj_in=entry_schema, db=db)
                    except IntegrityError:
                        db.rollback()
                        word = (
                            db.query(models.Word)
                            .filter(models.Word.lexeme == entry_schema.lexeme)
                            .filter(models.Word.language_code == entry_schema.language_code)
                            .first()
                        )
                        if not word:
                            raise

                # Link user -> word (users_words). UniqueConstraint prevents duplicates.
                try:
                    user_relation_crud.create(
                        obj_in=vocap_schemas.UserWordCreate(user_id=user.id, word_id=word.id),
                        db=db,
                    )
                except IntegrityError:
                    db.rollback()  # already linked; ignore

                # Handle mapped (related) words
                for mapped_schema in word_mapper.translations:
                    # mapped_schema is vocap_schemas.WordCreate
                    existing_mapped: Optional[models.Word] = (
                        db.query(models.Word)
                        .filter(models.Word.lexeme == mapped_schema.lexeme)
                        .filter(models.Word.language_code == mapped_schema.language_code)
                        .first()
                    )

                    if existing_mapped:
                        mapped_word = existing_mapped
                    else:
                        try:
                            mapped_word = word_crud.create(obj_in=mapped_schema, db=db)
                        except IntegrityError:
                            db.rollback()
                            mapped_word = (
                                db.query(models.Word)
                                .filter(models.Word.lexeme == mapped_schema.lexeme)
                                .filter(models.Word.language_code == mapped_schema.language_code)
                                .first()
                            )
                            if not mapped_word:
                                raise

                    # create the relation (word -> mapped_word), relation_type defaults to "translation"
                    try:
                        word_relation_crud.create(
                            obj_in=vocap_schemas.WordRelationCreate(
                                word_id=word.id,
                                related_word_id=mapped_word.id,
                                relation_type="TRANSLATION",
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