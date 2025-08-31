from dataclasses import dataclass, field as dc_field
from typing import List
from abc import ABC, abstractmethod

from ..schemas import UserBase, LexicalEntryBase, LexicalEntryBase


@dataclass
class EntryTranslationMapper:
    entry: LexicalEntryBase
    translations: List[LexicalEntryBase] = dc_field(default_factory=[])


@dataclass
class UserEntryMapper:
    user: UserBase
    entries: List[EntryTranslationMapper] = dc_field(default_factory=[])


# @dataclass
# class SeedData:
#     users: List[UserCreate]
#     lexical_entries: List[LexicalEntryCreate]
# extend as needed


class SeederInterface(ABC):
    @abstractmethod
    def load_data(self) -> List[UserEntryMapper]:
        """Should return a list of insertable database objects."""
        pass
