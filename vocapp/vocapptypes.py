from pydantic import BaseModel, Field
from typing import Literal, Iterable
from uuid import UUID, uuid4

Category = Literal['neutral', 'formal', 'informal']  # Define allowed categories


class Translation(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # Automatically generate a unique ID
    text: str
    category: Category = Field(default='neutral') # Use the custom type


class LexicalEntry(BaseModel):
    id: UUID = Field(default_factory=uuid4)  # Automatically generate a unique ID
    word: str
    translations: Iterable[Translation] = Field(default_factory=list)  # List of translations
