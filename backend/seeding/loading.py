from dataclasses import dataclass, field as dc_field
from typing import List
from abc import ABC, abstractmethod

from ..schemas import UserCreate, WordCreate


@dataclass
class LexemeWithTranslations:
    lexeme: WordCreate
    translations: List[WordCreate] = dc_field(default_factory=[])


@dataclass
class UserLexicon:
    user: UserCreate
    vocabulary: List[LexemeWithTranslations] = dc_field(default_factory=[])


class DataLoader(ABC):
    @abstractmethod
    def load_data(self) -> List[UserLexicon]:
        """Should return a list of insertable database objects."""
        pass