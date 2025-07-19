from pydantic import BaseModel, Field
from typing import Literal, Iterable
from uuid import UUID, uuid4

Category = Literal['neutral', 'formal', 'informal']  # Define allowed categories
Wordpack = Literal['basic', 'furniture']  # Define allowed wordpacks

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # Automatically generate a unique ID
    username: str
    password: str
    
class Translation(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # Automatically generate a unique ID
    lexeme: str
    category: Category = Field(default='neutral') # Use the custom type
    wordpack: Wordpack = Field(default='basic')  # Use the custom type


class LexicalEntry(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # Automatically generate a unique ID
    word: str
    translations: Iterable[Translation] = Field(default_factory=list)  # List of translations

