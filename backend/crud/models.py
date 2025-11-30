__ALL__ = ["user_crud", "entry_crud", "translation_crud", "entry_translation_crud"]

from .crud import CRUDBase
from ..models import *
from .. import schemas as vocap_schemas
from ..security import get_password_hash

field_transformers = {"password": lambda pw: {"hashed_password": get_password_hash(pw)}}

user_crud = CRUDBase[User, vocap_schemas.UserCreate](
    User, field_transformers=field_transformers
)
word_crud = CRUDBase[Word, vocap_schemas.WordCreate](
    Word, field_transformers=field_transformers
)
word_relation_crud = CRUDBase[WordRelation, vocap_schemas.WordRelationCreate](
    WordRelation, field_transformers=field_transformers
)
user_word_crud = CRUDBase[UserWord, vocap_schemas.UserWordCreate](
    UserWord, field_transformers=field_transformers
)
