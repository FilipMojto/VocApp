from pydantic import BaseModel, Field

from .vocap_db_types import TranslationCategory, Wordpack

# <--- User ---> #

class UserBase(BaseModel):
    
    username: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


# <--- LexicalEntry ---> #

class LexicalEntryBase(BaseModel):
    lexeme: str

class LexicalEntryCreate(LexicalEntryBase):
    user_id: int
    pass

class LexicalEntry(LexicalEntryBase):
    
    class Config:
        orm_mode = True

# <--- Translation ---> #

class TranslationBase(BaseModel):
    lexeme: str
    category: TranslationCategory = Field(default=TranslationCategory.NEUTRAL)
    wordpack: Wordpack = Field(default=Wordpack.BASIC)

class TranslationCreate(TranslationBase):
    # entry_id: int
    pass

class Translation(TranslationBase):

    class Config:
        orm_mode = True

# <--- EntryTranslationMapping ---> #

class EntryTranslationBase(BaseModel):
    pass

class EntryTranslationCreate(EntryTranslationBase):
    entry_id: int
    translation_id: int

class EntryTranslation(EntryTranslationBase):
    
    class Config:
        orm_mode = True

