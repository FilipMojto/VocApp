# import json

# from typing import List
# import os

# from .base import SeederInterface, UserEntryMapper, WordMapper
# from ..vocap_db_types import WordCategory, Wordpack
# from .. import schemas as vocap_schemas


# current_dir = os.path.dirname(__file__)
# VOCAB_FILE_PATH = os.path.abspath(os.path.join(current_dir, "../seeds/words.json"))


# class JSONLoader(SeederInterface):
#     """Seeder class for JSON files."""

#     def load_data(self, path: str = VOCAB_FILE_PATH) -> List[UserEntryMapper]:
#         with open(path, "r", encoding="utf-8") as file:
#             users_data = json.load(file)

#         user_entries: List[UserEntryMapper] = []

#         for user in users_data.get("users", []):
#             user_entries_obj = UserEntryMapper(
#                 user=vocap_schemas.UserBase(
#                     username=user["name"],
#                     password=user["password"],
#                 ),
#                 entries=[],
#             )

#             for entry in user.get("entries", []):
#                 entry_trans_obj = WordMapper(
#                     vocap_schemas.LexicalEntryBase(lexeme=entry["lexeme"]),
#                     translations=[],
#                 )

#                 for translation in entry.get("translations", []):
#                     entry_trans_obj.translations.append(
#                         vocap_schemas.TranslationBase(
#                             lexeme=translation["lexeme"],
#                             category=WordCategory[
#                                 translation["category"].upper()
#                             ],
#                             wordpack=Wordpack[translation["wordpack"].upper()],
#                         )
#                     )

#                 user_entries_obj.entries.append(entry_trans_obj)

#             user_entries.append(user_entries_obj)

#         return user_entries

import json
from typing import List
import os

from .base import SeederInterface, UserEntryMapper, WordMapper
from ..vocap_db_types import WordCategory, Wordpack
from .. import schemas as vocap_schemas

current_dir = os.path.dirname(__file__)
VOCAB_FILE_PATH = os.path.abspath(os.path.join(current_dir, "../seeds/words.json"))


class JSONLoader(SeederInterface):
    """Seeder class for JSON files (expects structure: { "users": [ { "name", "password", "words": [...] } ] })"""

    def load_data(self, path: str = VOCAB_FILE_PATH) -> List[UserEntryMapper]:
        with open(path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        users_list = raw.get("users") if isinstance(raw, dict) else (raw if isinstance(raw, list) else [])
        result: List[UserEntryMapper] = []

        for user_obj in users_list:
            username = user_obj.get("name") or user_obj.get("username")
            password = user_obj.get("password") or user_obj.get("passwd") or ""

            # Create a Pydantic UserCreate object (fits your seeder pipeline)
            user_schema = vocap_schemas.UserCreate(username=username, password=password)

            user_mapper = UserEntryMapper(user=user_schema, entries=[])

            for word_obj in user_obj.get("words", []):
                lexeme = word_obj.get("lexeme")
                language_code = word_obj.get("language_code") or word_obj.get("lang") or "en"
                print(f"language_code: {language_code}")
                category_str = (word_obj.get("category") or "neutral").upper()
                pack_str = (word_obj.get("wordpack") or "basic").upper()

                # map to enums safely, fallback to defaults
                try:
                    category_enum = WordCategory[category_str]
                except Exception:
                    category_enum = WordCategory.NEUTRAL

                try:
                    pack_enum = Wordpack[pack_str]
                except Exception:
                    pack_enum = Wordpack.BASIC

                entry_schema = vocap_schemas.WordCreate(
                    lexeme=lexeme,
                    language_code=language_code,
                    category=category_enum,
                    wordpack=pack_enum,
                )

                word_mapper = WordMapper(entry=entry_schema, translations=[])

                for mapped in word_obj.get("mapped_words", []):
                    m_lex = mapped.get("lexeme")
                    m_lang = mapped.get("language_code") or mapped.get("lang") or "en"
                    m_cat_str = (mapped.get("category") or "neutral").upper()
                    m_pack_str = (mapped.get("wordpack") or "basic").upper()

                    try:
                        m_cat_enum = WordCategory[m_cat_str]
                    except Exception:
                        m_cat_enum = WordCategory.NEUTRAL

                    try:
                        m_pack_enum = Wordpack[m_pack_str]
                    except Exception:
                        m_pack_enum = Wordpack.BASIC

                    mapped_schema = vocap_schemas.WordCreate(
                        lexeme=m_lex,
                        language_code=m_lang,
                        category=m_cat_enum,
                        wordpack=m_pack_enum,
                    )

                    word_mapper.translations.append(mapped_schema)

                user_mapper.entries.append(word_mapper)

            result.append(user_mapper)

        return result