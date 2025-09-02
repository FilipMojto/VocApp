from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib import import_module
import sqlite3
import os, sys
from typing import List
from sqlalchemy.orm import Session

# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

# from .models import User, LexicalEntry, Translation, EntryTranslation
from .loaders.base import SeederInterface
from .loaders.json import JSONLoader
from .crud import crud as vocap_crud
from . import schemas as vocap_schemas
from .crud.models import *

DB_PATH = "./vocapp.db"
SUPPORTED_SEEDERS = ["json"]


def seed_data(seeder: str, db: Session):
    print("Seeding data...")
    """Seed the database with initial data."""
    if seeder not in SUPPORTED_SEEDERS:
        raise ValueError(
            f"Unsupported seeder format: {seeder}. Supported formats: {SUPPORTED_SEEDERS}"
        )

    module_instance: SeederInterface = None

    match seeder:
        case "json":
            module_instance = JSONLoader()
        case _:
            raise ValueError(
                f"Unsupported seeder format: {seeder}. Supported formats: {SUPPORTED_SEEDERS}"
            )

    seed_data = module_instance.load_data()
    print("seed:\n", seed_data)

    # Insert users into the database
    for user_entry_obj in seed_data:
        user = user_crud.create(
            db=db, obj_in=vocap_schemas.UserCreate(**user_entry_obj.user.model_dump())
        )

        for entry_trans_obj in user_entry_obj.entries:
            entry = word_crud.create(
                db=db,
                obj_in=vocap_schemas.LexicalEntryCreate(
                    user_id=user.id, **entry_trans_obj.entry.model_dump()
                ),
            )

            for translation_obj in entry_trans_obj.translations:
                # Check if translation already exists
                existing = translation_crud.get_by_lexeme(
                    db=db, lexeme=translation_obj.lexeme
                )

                if existing:
                    translation = existing
                else:
                    translation = translation_crud.create(
                        db=db,
                        obj_in=vocap_schemas.TranslationCreate(
                            **translation_obj.model_dump()
                        ),
                    )

                # translation = translation_crud.create(db=db, obj_in=vocap_schemas.TranslationCreate(**translation_obj.model_dump()))
                word_relation_crud.create(
                    db=db,
                    obj_in=vocap_schemas.WordRelationCreate(
                        entry_id=entry.id, translation_id=translation.id
                    ),
                )

    db.commit()
