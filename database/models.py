# __ALL__ = ["User", "LexicalEntry", "Translation", "EntryTranslation"]
__ALL__ = ["User", "Word", "UserWord", "WordRelation"]

from sqlalchemy import Integer, Column, PrimaryKeyConstraint, String, ForeignKey, Table, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy

from .dbconfig import Base
from .vocap_db_types import WordCategory, Wordpack, WordLanguageCode, WordRelationType


# class User(Base):
#     __tablename__ = "users"

#     id = Column(Integer, primary_key=True)
#     username = Column(String, index=True, nullable=False, unique=True)
#     password = Column(String, index=True, nullable=False)
#     hashed_password = Column(String, index=True, nullable=False)

#     lexical_entries = relationship(
#         "LexicalEntry", back_populates="owner", cascade="all, delete"
#     )


# class LexicalEntry(Base):
#     __tablename__ = "lexical_entries"

#     id = Column(Integer, primary_key=True, index=True)
#     lexeme = Column(String, index=True, nullable=False, unique=True)

#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

#     owner = relationship("User", back_populates="lexical_entries")
#     translations = association_proxy("entry_links", "translation")


# class Translation(Base):
#     __tablename__ = "translations"

#     id = Column(Integer, primary_key=True, index=False)
#     lexeme = Column(String, index=True, nullable=False, unique=True)
#     category = Column(
#         Enum(TranslationCategory), nullable=False, default=TranslationCategory.NEUTRAL
#     )
#     wordpack = Column(Enum(Wordpack), nullable=False, default=Wordpack.BASIC)
#     entries = association_proxy("translation_links", "entry")


# class EntryTranslation(Base):
#     __tablename__ = "entries_translations"

#     entry_id = Column(Integer, ForeignKey("lexical_entries.id"), primary_key=True)
#     translation_id = Column(Integer, ForeignKey("translations.id"), primary_key=True)

#     entry = relationship("LexicalEntry", backref="entry_links")
#     translation = relationship("Translation", backref="translation_links")


# --- User ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, nullable=False, unique=True)
    password = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    words = relationship("UserWord", back_populates="user", cascade="all, delete")


# --- Word ---
class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    lexeme = Column(String, index=True, nullable=False)
    language_code = Column(String(2), nullable=False)
    category = Column(Enum(WordCategory), nullable=True)
    wordpack = Column(Enum(Wordpack), nullable=True)

    __table_args__ = (
        UniqueConstraint("lexeme", "language_code", name="uq_lexeme_language"),
    )

    users = relationship("UserWord", back_populates="word", cascade="all, delete")
    relations = relationship(
        "WordRelation",
        foreign_keys="WordRelation.word_id",
        back_populates="word",
        cascade="all, delete"
    )
    related_to = relationship(
        "WordRelation",
        foreign_keys="WordRelation.related_word_id",
        back_populates="related_word",
        cascade="all, delete"
    )


# --- UserWord ---
class UserWord(Base):
    __tablename__ = "users_words"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "word_id", name="uq_user_word"),
    )

    user = relationship("User", back_populates="words")
    word = relationship("Word", back_populates="users")


# --- WordRelation ---
class WordRelation(Base):
    __tablename__ = "words_relations"

    word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    related_word_id = Column(Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False)
    relation_type = Column(
        Enum(WordRelationType),
        nullable=False,
    )

    __table_args__ = (
        PrimaryKeyConstraint("word_id", "related_word_id", "relation_type", name="pk_word_relation"),
    )

    word = relationship("Word", foreign_keys=[word_id], back_populates="relations")
    related_word = relationship("Word", foreign_keys=[related_word_id], back_populates="related_to")