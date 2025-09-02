__ALL__ = ["user_crud", "entry_crud", "translation_crud", "entry_translation_crud"]

from .crud import CRUDBase
from ..models import *
from .. import schemas as vocap_schemas

user_crud = CRUDBase[User, vocap_schemas.UserCreate](User)
word_crud = CRUDBase[Word, vocap_schemas.WordCreate](Word)
# translation_crud = CRUDBase[Translation, vocap_schemas.TranslationCreate](Translation)
word_relation_crud = CRUDBase[
    WordRelation, vocap_schemas.WordRelationCreate
](WordRelation)
user_relation_crud = CRUDBase[
    UserWord, vocap_schemas.UserWordCreate
](UserWord)

