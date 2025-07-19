from sqlalchemy.orm import Session
from .. import models, schemas
from ..models import *
from .. import schemas as vocap_schemas

# <--- Users ---> #

# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()

# def get_users(db: Session, skip: int = 0, limit: int = 10):
#     return db.query(models.User).offset(skip).limit(limit).all()

# def create_user(db: Session, user: schemas.UserCreate):
#     db_user = models.User(**user.model_dump())
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user

# # <--- Lexical Entries ---> #

# def create_lexical_entry(db: Session, entry: schemas.LexicalEntryCreate):
#     db_entry = models.LexicalEntry(**entry.model_dump())
#     db.add(db_entry)
#     db.commit()
#     db.refresh(db_entry)
#     return db_entry

from typing import Generic, TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 10) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def get_by_lexeme(self, db: Session, lexeme: str) -> Optional[ModelType]:
        """
            Use only on tables LexicalEntries and Translations
        """
        return db.query(self.model).filter(self.model.lexeme == lexeme).first()

