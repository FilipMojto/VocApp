from abc import ABC, abstractmethod
from dataclasses import dataclass
from importlib import import_module
import sqlite3
import os, sys
from typing import List
from sqlalchemy.orm import Session

# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

from .models import User, LexicalEntry, Translation, EntryTranslation
from .loaders.base import SeederInterface
from .loaders.json import JSONLoader
from .crud import crud as vocap_crud
from . import schemas as vocap_schemas
from .crud.models import *

DB_PATH = './vocapp.db'
SUPPORTED_SEEDERS = ['json']    


def seed_data(seeder: str, conn: sqlite3.Connection, db: Session):
    print("Seeding data...")
    """Seed the database with initial data."""
    if seeder not in SUPPORTED_SEEDERS:
        raise ValueError(f"Unsupported seeder format: {seeder}. Supported formats: {SUPPORTED_SEEDERS}")
    
    # Import the appropriate seeder based on the file name
    # module_name = f"database.seeders.{seeder.split('.')[0]}"
    # module = import_module(module_name)

    module_instance: SeederInterface = None
    
    match seeder:
        case 'json':
            module_instance = JSONLoader()
        case _:
            raise ValueError(f"Unsupported seeder format: {seeder}. Supported formats: {SUPPORTED_SEEDERS}")
        
    seed_data = module_instance.load_data()
    # user_crud = vocap_crud.CRUDBase[User, vocap_schemas.UserCreate](User)
    # entry_crud = vocap_crud.CRUDBase[LexicalEntry, vocap_schemas.LexicalEntryCreate](LexicalEntry)
    # translation_crud = vocap_crud.CRUDBase[Translation, vocap_schemas.TranslationCreate](Translation)
    # entry_translation_crud = vocap_crud.CRUDBase[EntryTranslation, vocap_schemas.EntryTranslationCreate](EntryTranslation)

    # cursor = conn.cursor()

    # Insert users into the database
    for user_entry_obj in seed_data:
        # user_crud = vocap_crud.CRUDBase[User, vocap_schemas.UserCreate](User)
        user = user_crud.create(db=db, obj_in=vocap_schemas.UserCreate(**user_entry_obj.user.model_dump()))
        
        # user_crud.create_user(db=db, user=user_entry_obj.user)

        for entry_trans_obj in user_entry_obj.entries:
            # vocap_crud.create
            # entry_crud = vocap_crud.CRUDBase[LexicalEntry, vocap_schemas.LexicalEntryCreate](LexicalEntry)
            entry = entry_crud.create(db=db, obj_in=vocap_schemas.LexicalEntryCreate(user_id=user.id, **entry_trans_obj.entry.model_dump()))

            for translation_obj in entry_trans_obj.translations:
                # Check if translation already exists
                existing = translation_crud.get_by_lexeme(db=db, lexeme=translation_obj.lexeme)
                
                if existing:
                    translation = existing
                else:
                    translation = translation_crud.create(
                        db=db,
                        obj_in=vocap_schemas.TranslationCreate(**translation_obj.model_dump())
                    )

                # translation = translation_crud.create(db=db, obj_in=vocap_schemas.TranslationCreate(**translation_obj.model_dump()))
                entry_translation_crud.create(db=db, obj_in=vocap_schemas.EntryTranslationCreate(entry_id=entry.id, translation_id=translation.id))

         
