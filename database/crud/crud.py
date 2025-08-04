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

from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseModel

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=vocap_schemas.VocapCreate)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=vocap_schemas.VocapUpdate)
# DeleteSchemaType = TypeVar("DeleteSchemaType", bound=vocap_schemas.VocapDelete)

class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, id: int, db: Session) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 10) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: CreateSchemaType, db: Session) -> ModelType:
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        try:
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            return db_obj
        except IntegrityError as e:
            db.rollback()
            raise e

    
    def get_by_lexeme(self, lexeme: str, db: Session) -> Optional[ModelType]:
        """
            Use only on tables LexicalEntries and Translations
        """

        return db.query(self.model).filter(self.model.lexeme == lexeme).first()
    
    def get_by_col_value(self, col: str, value: Any, db: Session, many: bool = False):
        if not hasattr(self.model, col):
            raise ValueError(f"Column '{col}' does not exist on model '{self.model.__name__}'")

        column_attr = getattr(self.model, col)

        print("col_attr", type(column_attr))
        print("val_attr", type(value))
        
        # if type(column_attr) != type(value):
        #     raise TypeError("Specified column's type doesn't match the value's type.")

        query = db.query(self.model).filter(column_attr == value)
        return query.all() if many else query.first()

    
    def update(self, obj_in: UpdateSchemaType, db: Session):
        """_summary_

        Args:
            obj_in (UpdateSchemaType): _description_
            db (Session, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        
        # Get the existing object by its ID
        db_obj = db.query(self.model).get(obj_in.id)
        if not db_obj:
            return None

        # Update the fields
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, id: int, db: Session):
        db_obj = db.query(self.model).get(id)
        if not db_obj:
            return None

        db.delete(db_obj)
        db.commit()
        return db_obj