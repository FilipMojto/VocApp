# from pydantic import BaseModel, Field

# from .vocap_db_types import WordCategory, Wordpack

# # ─────────────────────────────────────────────
# # SECTION: Schemas
# # ─────────────────────────────────────────────

# # === Generic Schemas ===


# class Identity(BaseModel):
#     id: int


# class VocapCreate(BaseModel):
#     pass


# class VocapUpdate(BaseModel):
#     pass


# class VocapReturn(BaseModel):
#     pass


# # === User ===


# class UserBase(BaseModel):
#     username: str
#     password: str


# class UserCreate(VocapCreate, UserBase):
#     pass


# class UserUpdate(VocapUpdate, UserBase, Identity):
#     # id: int
#     pass


# class User(VocapReturn, UserBase, Identity):
#     hashed_password: str

#     class Config:
#         orm_mode = True


# # For returning user info


# class UserReturn(Identity):
#     username: str

#     class Config:
#         orm_mode = True


# # === Lexical Entry ===


# class LexicalEntryBase(BaseModel):
#     lexeme: str


# class LexicalEntryCreate(LexicalEntryBase):
#     user_id: int
#     # pass


# class LexicalEntry(LexicalEntryBase, Identity):

#     class Config:
#         orm_mode = True


# class LexicalEntryUpdate(VocapUpdate, LexicalEntryBase, Identity):
#     pass


# # === Translation ===


# class TranslationBase(BaseModel):
#     lexeme: str
#     category: WordCategory = Field(default=WordCategory.NEUTRAL)
#     wordpack: Wordpack = Field(default=Wordpack.BASIC)


# class TranslationCreate(VocapCreate, TranslationBase):
#     # user_id: int
#     pass


# class TranslationUpdate(VocapUpdate, TranslationBase, Identity):
#     pass


# class Translation(TranslationBase, Identity):

#     class Config:
#         orm_mode = True


# # === EntryTranslation ===


# class EntryTranslationBase(BaseModel):
#     entry_id: int
#     translation_id: int
#     # user_id: int


# class EntryTranslationCreate(VocapCreate, EntryTranslationBase):
#     pass


# class EntryTranslationUpdate(VocapUpdate, EntryTranslationBase):
#     pass


# class EntryTranslation(EntryTranslationBase):

#     class Config:
#         orm_mode = True

from typing import Optional
from pydantic import BaseModel, Field
from .vocap_db_types import WordCategory, Wordpack, WordLanguageCode

# ───────────────────────────────
# Generic Schemas
# ───────────────────────────────
class Identity(BaseModel):
    id: int


class VocapCreate(BaseModel):
    pass


class VocapUpdate(BaseModel):
    pass


class VocapReturn(BaseModel):
    pass


# ───────────────────────────────
# User
# ───────────────────────────────
class UserBase(BaseModel):
    username: str


class UserCreate(VocapCreate, UserBase):
    password: str  # client provides plain password


class UserUpdate(VocapUpdate):
    username: Optional[str] = None
    password: Optional[str] = None


class UserReturn(Identity, UserBase):
    class Config:
        orm_mode = True


# ───────────────────────────────
# Word
# ───────────────────────────────
class WordBase(BaseModel):
    lexeme: str
    language_code: WordLanguageCode = Field(default=WordLanguageCode.EN)
    category: WordCategory = Field(default=WordCategory.NEUTRAL)
    wordpack: Wordpack = Field(default=Wordpack.BASIC)


class WordCreate(VocapCreate, WordBase):
    pass


class WordUpdate(VocapUpdate):
    lexeme: Optional[str] = None
    language_code: Optional[WordLanguageCode] = None
    category: Optional[WordCategory] = None
    wordpack: Optional[Wordpack] = None


class WordReturn(Identity, WordBase):
    class Config:
        orm_mode = True


# ───────────────────────────────
# UserWord
# ───────────────────────────────
class UserWordBase(BaseModel):
    user_id: int
    word_id: int


class UserWordCreate(VocapCreate, UserWordBase):
    pass


class UserWordUpdate(VocapUpdate):
    user_id: Optional[int] = None
    word_id: Optional[int] = None


class UserWordReturn(Identity, UserWordBase):
    class Config:
        orm_mode = True


# ───────────────────────────────
# WordRelation
# ───────────────────────────────
class WordRelationBase(BaseModel):
    word_id: int
    related_word_id: int
    relation_type: str


class WordRelationCreate(VocapCreate, WordRelationBase):
    pass


class WordRelationUpdate(VocapUpdate):
    related_word_id: Optional[int] = None
    relation_type: Optional[str] = None


class WordRelationReturn(WordRelationBase):
    class Config:
        orm_mode = True

# class User(VocapReturn, UserBase, Identity):
#     class Config:
#         orm_mode = True





