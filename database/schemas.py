from pydantic import BaseModel, Field

from .vocap_db_types import TranslationCategory, Wordpack

# ─────────────────────────────────────────────
# SECTION: Schemas
# ─────────────────────────────────────────────

# === Generic Schemas ===


class Identity(BaseModel):
    id: int


class VocapCreate(BaseModel):
    pass


class VocapUpdate(BaseModel):
    pass


class VocapReturn(BaseModel):
    pass


# === User ===


class UserBase(BaseModel):
    username: str
    password: str


class UserCreate(VocapCreate, UserBase):
    pass


class UserUpdate(VocapUpdate, UserBase, Identity):
    # id: int
    pass


class User(VocapReturn, UserBase, Identity):
    hashed_password: str

    class Config:
        orm_mode = True


# For returning user info


class UserReturn(Identity):
    username: str

    class Config:
        orm_mode = True


# === Lexical Entry ===


class LexicalEntryBase(BaseModel):
    lexeme: str


class LexicalEntryCreate(LexicalEntryBase):
    user_id: int


class LexicalEntry(LexicalEntryBase, Identity):

    class Config:
        orm_mode = True


class LexicalEntryUpdate(VocapUpdate, LexicalEntryBase, Identity):
    pass


# === Translation ===


class TranslationBase(BaseModel):
    lexeme: str
    category: TranslationCategory = Field(default=TranslationCategory.NEUTRAL)
    wordpack: Wordpack = Field(default=Wordpack.BASIC)


class TranslationCreate(VocapCreate, TranslationBase):
    user_id: int


class TranslationUpdate(VocapUpdate, TranslationBase, Identity):
    pass


class Translation(TranslationBase, Identity):

    class Config:
        orm_mode = True


# === EntryTranslation ===


class EntryTranslationBase(BaseModel):
    entry_id: int
    translation_id: int


class EntryTranslationCreate(VocapCreate, EntryTranslationBase):
    pass


class EntryTranslationUpdate(VocapUpdate, EntryTranslationBase):
    pass


class EntryTranslation(EntryTranslationBase):

    class Config:
        orm_mode = True
