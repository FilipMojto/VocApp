__ALL__ = ['User', 'LexicalEntry', 'Translation', 'EntryTranslation']

from sqlalchemy import Integer, Column, String, ForeignKey, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .dbconfig import Base
from .vocap_db_types import TranslationCategory, Wordpack

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, index=True, nullable=False)

    lexical_entries = relationship("LexicalEntry", back_populates="owner", cascade="all, delete")


# entries_translations = Table(
#     "entries_translations",
#     Base.metadata,
#     Column("entry_id", ForeignKey("lexical_entries.id"), primary_key=True),
#     Column("translation_id", ForeignKey("translations.id"), primary_key=True)
# )


class LexicalEntry(Base):
    __tablename__ = "lexical_entries"

    id = Column(Integer, primary_key=True, index=True)
    lexeme = Column(String, index=True, nullable=False, unique=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="lexical_entries")

    # translations = relationship("Translation", secondary=entries_translations, back_populates="entries")
    translations = association_proxy("entry_links", "translation")


class Translation(Base):
    __tablename__ = "translations"

    id = Column(Integer, primary_key=True, index=False)
    lexeme = Column(String, index=True, nullable=False, unique=True)
    category = Column(Enum(TranslationCategory), nullable=False, default=TranslationCategory.NEUTRAL)
    wordpack = Column(Enum(Wordpack), nullable=False, default=Wordpack.BASIC)
    # entries = relationship("LexicalEntry", secondary=entries_translations, back_populates="translations")
    entries = association_proxy("translation_links", "entry")



class EntryTranslation(Base):
    __tablename__ = "entries_translations"

    entry_id = Column(Integer, ForeignKey("lexical_entries.id"), primary_key=True)
    translation_id = Column(Integer, ForeignKey("translations.id"), primary_key=True)

    entry = relationship("LexicalEntry", backref="entry_links")
    translation = relationship("Translation", backref="translation_links")