__ALL__ = ['user_crud', 'entry_crud', 'translation_crud', 'entry_translation_crud']

from .crud import CRUDBase
from ..models import *
from .. import schemas as vocap_schemas

user_crud = CRUDBase[User, vocap_schemas.UserCreate](User)
entry_crud = CRUDBase[LexicalEntry, vocap_schemas.LexicalEntryCreate](LexicalEntry)
translation_crud = CRUDBase[Translation, vocap_schemas.TranslationCreate](Translation)
entry_translation_crud = CRUDBase[EntryTranslation, vocap_schemas.EntryTranslationCreate](EntryTranslation)
