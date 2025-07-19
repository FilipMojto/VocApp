from typing import Iterable

from shared.vocapptypes import LexicalEntry

class PersonalVocabulary:

    def __init__(self, vocabulary: Iterable[LexicalEntry] = None):
        self.vocabulary = vocabulary if vocabulary is not None else []
        self._id_counter = 0
    
    def add_entry(self, entry: LexicalEntry):
        """Add a new lexical entry to the vocabulary."""
        self.vocabulary.append(entry)
    
    def get_entry(self, word: str) -> LexicalEntry:
        """Retrieve a lexical entry by word."""
        for entry in self.vocabulary:
            if entry.word == word:
                return entry
            
        raise ValueError(f"Entry for word '{word}' not found.")
    
    def remove_entry(self, word: str):
        """Remove a lexical entry by word."""
        for entry in self.vocabulary:
            if entry.word == word:
                self.vocabulary.remove(entry)
                return
        
        raise ValueError(f"Entry for word '{word}' not found.")
