from enum import Enum as PyEnum


class WordCategory(PyEnum):
    NEUTRAL = "neutral"
    FORMAL = "formal"
    INFORMAL = "informal"
    IDIOMATIC = "idomatic"


class Wordpack(PyEnum):
    BASIC = "basic"
    FURNITURE = "furniture"


class WordRelationType(PyEnum):
    TRANSLATION = "translation"
    SYNONYM = "synonym"
    ANTONYM = "antonym"
    DERIVED = "derived"
    CUSTOM = "custom"

class WordLanguageCode(PyEnum):
    EN = "en"
    DE = "de"
    FR = "fr"
    ES = "es"
    IT = "it"
    PT = "pt"
    RU = "ru"
    ZH = "zh"
    JA = "ja"
    KO = "ko"
    AR = "ar"
    HI = "hi"
    SW = "sw"
    NL = "nl"
    SV = "sv"
    NO = "no"
    DA = "da"
    FI = "fi"
    PL = "pl"
    CS = "cs"
    HU = "hu"
    RO = "ro"
    TR = "tr"
    EL = "el"
    HE = "he"
    TH = "th"
    VI = "vi"
