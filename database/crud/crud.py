from sqlalchemy.orm import Session
from ..models import *
from .. import schemas as vocap_schemas

from typing import Callable, Dict, Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=vocap_schemas.VocapCreate)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=vocap_schemas.VocapUpdate)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(
        self,
        model: Type[ModelType],
        field_transformers: Optional[Dict[str, Callable[[Any], Any]]] = None,
    ):
        self.model = model
        self.field_transformers = field_transformers

    def __apply_field_transformers(self, obj_data: Dict[str, Any]):
        """
        Field transformers may be provided in three forms:
          1) {"password": some_callable} -> replaces obj_data["password"] with callable(value)
          2) {"password": ("hashed_password", some_callable)} -> sets obj_data["hashed_password"] = callable(value) and removes obj_data["password"]
          3) {"password": some_callable_returning_dict} -> merges the returned dict into obj_data and removes original "password"
        """
        if not self.field_transformers:
            return

        for field, transformer in self.field_transformers.items():
            if field not in obj_data:
                continue

            # form (2): tuple (target_name, fn)
            if isinstance(transformer, (tuple, list)) and len(transformer) == 2 and callable(transformer[1]):
                target_name, fn = transformer[0], transformer[1]
                new_val = fn(obj_data[field])
                obj_data[target_name] = new_val
                # remove original if different
                if target_name != field:
                    obj_data.pop(field, None)
                continue

            # form (1) or (3): callable
            if callable(transformer):
                res = transformer(obj_data[field])
                # if callable returned a dict, merge it
                if isinstance(res, dict):
                    obj_data.update(res)
                    # remove original field (we assume transformer provided replacements)
                    obj_data.pop(field, None)
                else:
                    # simple replace in-place
                    obj_data[field] = res
                continue

            # unexpected transformer type
            raise TypeError(f"Unsupported transformer for field '{field}': {transformer!r}")
        

    def get(self, id: int, db: Session) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(self, db: Session, skip: int = 0, limit: int = 10) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, obj_in: CreateSchemaType, db: Session) -> ModelType:
        obj_data = obj_in.model_dump()
        self.__apply_field_transformers(obj_data=obj_data)
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
            raise ValueError(
                f"Column '{col}' does not exist on model '{self.model.__name__}'"
            )

        column_attr = getattr(self.model, col)
        query = db.query(self.model).filter(column_attr == value)
        return query.all() if many else query.first()

    def update(self, db: Session, db_obj: ModelType, obj_in: UpdateSchemaType):
        update_data = obj_in.model_dump(exclude_unset=True)
        self.__apply_field_transformers(obj_data=update_data)

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
