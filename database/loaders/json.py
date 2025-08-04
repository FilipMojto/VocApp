
import json

from typing import List
import os, sys

# Ensure the path to the seeds directory is in the system path
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
# sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../..')

from .base import SeederInterface, UserEntryMapper, EntryTranslationMapper
# from shared.vocapptypes import LexicalEntry, Translation, User, Category, Wordpack
from ..vocap_db_types import TranslationCategory, Wordpack
from .. import schemas as vocap_schemas

# VOCAB_FILE_PATH = '../seeds/words.json'
current_dir = os.path.dirname(__file__)
VOCAB_FILE_PATH = os.path.abspath(os.path.join(current_dir, "../seeds/words.json"))

# LEXICAL_ENTRIES_FILE_PATH = './seeds/lexical_entries.json'


# def load_users_json() -> List[User]:
#     SEEDER_FILE_PATH = './seeds/users.json'
    
#     with open(SEEDER_FILE_PATH, 'r', encoding='utf-8') as file:
#         users_data = json.load(file)

#     users: List[User] = []

#     for user in users_data.get('users', []):
#         user_obj = User(
#             id=user.get('id'),
#             username=user['name'],
#             password=user['password']
#         )
#         users.append(user_obj)

#     return users


# def load_lexical_entries_json() -> List[LexicalEntry]:
#     SEEDER_FILE_PATH = './seeds/lexical_entries.json'
    
#     with open(SEEDER_FILE_PATH, 'r', encoding='utf-8') as file:
#         lexical_entries_data = json.load(file)

#     lexical_entries: List[LexicalEntry] = []

#     for entry in lexical_entries_data.get('entries', []):
#         translations = entry.get('translations', [])
#         translation_objects = [
#             Translation(
#                 lexeme=translation['text'],
#                 category=translation.get('category', 'neutral'),
#                 wordpack=translation.get('wordpack', 'basic')
#             ) for translation in translations
#         ]

#          # Create a LexicalEntry object with the word and its translations

#         lexical_entry = LexicalEntry(
#             word=entry['word'],
#             translations=translation_objects
#         )

#         lexical_entries.append(lexical_entry)

#     return lexical_entries



class JSONLoader(SeederInterface):
    """Seeder class for JSON files."""

    def load_data(self, path: str = VOCAB_FILE_PATH) -> List[UserEntryMapper]:
        with open(path, 'r', encoding='utf-8') as file:
            users_data = json.load(file)

        # users: List[vocap_schemas.UserCreate] = []
        user_entries: List[UserEntryMapper] = []

        for user in users_data.get('users', []):
            user_entries_obj = UserEntryMapper(
                user=vocap_schemas.UserBase(
                    # id=user.get('id'),
                    username=user['name'],  
                    password=user['password']
                ),
                entries=[]
            )

            # entry_trans: List[EntryTranslationMapper] = []

            for entry in user.get('entries', []):
                entry_trans_obj = EntryTranslationMapper(
                    vocap_schemas.LexicalEntryBase(
                        lexeme=entry['lexeme']
                    ),
                    translations=[]
                )

                for translation in entry.get('translations', []):
                    entry_trans_obj.translations.append(
                        vocap_schemas.TranslationBase(
                            lexeme=translation['lexeme'],
                            category=TranslationCategory[translation['category'].upper()],
                            wordpack=Wordpack[translation['wordpack'].upper()]
                        )
                    )
                
                user_entries_obj.entries.append(entry_trans_obj)
            
            user_entries.append(user_entries_obj)

        return user_entries