__ALL__ = ["User", "Word", "UserWord", "WordRelation"]

from sqlalchemy import (
    Integer,
    Column,
    PrimaryKeyConstraint,
    String,
    ForeignKey,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .dbconfig import Base
from .vocap_db_types import WordCategory, Wordpack, WordRelationType, WordLanguageCode


# --- User ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, index=True, nullable=False, unique=True)
    # password = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)

    # words = relationship("WordRelation", back_populates="user", cascade="all, delete")
    # link to UserWord (association)
    # user_words = relationship("UserWord", back_populates="user", cascade="all, delete")

    # optional: direct shortcut to words via secondary association
    words = relationship("Word", secondary="users_words", back_populates="users")

    # link to WordRelation (relations created by this user)
    word_relations = relationship("WordRelation", back_populates="user", cascade="all, delete")


# --- Word ---
class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    lexeme = Column(String, index=True, nullable=False)
    language_code = Column(Enum(WordLanguageCode), nullable=False)
    category = Column(Enum(WordCategory), nullable=True)
    wordpack = Column(Enum(Wordpack), nullable=True)

    __table_args__ = (
        UniqueConstraint("lexeme", "language_code", name="uq_lexeme_language"),
    )

    # link to UserWord
    # user_words = relationship("UserWord", back_populates="word", cascade="all, delete")

    # direct shortcut to users via secondary
    users = relationship("User", secondary="users_words", back_populates="words")


    # users = relationship("Word", back_populates="word", cascade="all, delete")
    relations = relationship(
        "WordRelation",
        foreign_keys="WordRelation.word_id",
        back_populates="word",
        cascade="all, delete",
    )
    related_to = relationship(
        "WordRelation",
        foreign_keys="WordRelation.related_word_id",
        back_populates="related_word",
        cascade="all, delete",
    )


# --- UserWord ---
class UserWord(Base):
    __tablename__ = "users_words"

    # id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    word_id = Column(
        Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            "user_id",
            "word_id",
            name="pk_user_word",
        ),
    )

    # __table_args__ = (UniqueConstraint("user_id", "word_id", name="uq_user_word"),)

    # user = relationship("User", back_populates="words")
    # word = relationship("Word", back_populates="users")
    # user = relationship("User", back_populates="user_words")
    # word = relationship("Word", back_populates="user_words")

# --- WordRelation ---
class WordRelation(Base):
    __tablename__ = "words_relations"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    word_id = Column(
        Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False
    )
    related_word_id = Column(
        Integer, ForeignKey("words.id", ondelete="CASCADE"), nullable=False
    )
    relation_type = Column(
        Enum(WordRelationType),
        nullable=False,
    )

    __table_args__ = (
        PrimaryKeyConstraint(
            "user_id",
            "word_id",
            "related_word_id",
            "relation_type",
            name="pk_word_relation",
        ),
    )

    # user = relationship("User", foreign_keys=[user_id], back_populates="words")
    user = relationship("User", foreign_keys=[user_id], back_populates="word_relations")

    word = relationship("Word", foreign_keys=[word_id], back_populates="relations")
    related_word = relationship(
        "Word", foreign_keys=[related_word_id], back_populates="related_to"
    )
