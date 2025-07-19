from enum import Enum as PyEnum


class TranslationCategory(PyEnum):
    NEUTRAL = "neutral"
    FORMAL = "formal"
    INFORMAL = "informal"
    IDIOMATIC = "idomatic"


class Wordpack(PyEnum):
    BASIC = "basic"
    FURNITURE = "furniture"
