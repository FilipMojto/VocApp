# Paste your schema as a single string
schema = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL UNIQUE,
    password VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS lexical_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lexeme VARCHAR(50) NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lexeme VARCHAR(50) NOT NULL UNIQUE,
    category VARCHAR(20),
    wordpack VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS entries_translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    translation_id INTEGER NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES LexicalEntry(id) ON DELETE CASCADE,
    FOREIGN KEY (translation_id) REFERENCES Translation(id) ON DELETE CASCADE,
    UNIQUE(entry_id, translation_id)
);
"""

# === v2 ===

schema_v2 = """
-- === Users ===
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- === Words ===
CREATE TABLE words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lexeme TEXT NOT NULL,
    language_code CHAR(2) NOT NULL,
    category TEXT,
    wordpack TEXT,
    UNIQUE (lexeme, language_code)
);

-- === Users ↔ Words ===
CREATE TABLE users_words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word_id INTEGER NOT NULL,
    UNIQUE (user_id, word_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE
);

-- === Enum simulation for relation_type ===
-- SQLite doesn’t support ENUM, so we use TEXT + CHECK
CREATE TABLE words_relations (
    word_id INTEGER NOT NULL,
    related_word_id INTEGER NOT NULL,
    relation_type TEXT NOT NULL CHECK (
        relation_type IN ('translation', 'synonym', 'antonym', 'derived', 'custom')
    ),
    PRIMARY KEY (word_id, related_word_id, relation_type),
    FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE,
    FOREIGN KEY (related_word_id) REFERENCES words(id) ON DELETE CASCADE
);

-- Helpful indexes for performance
CREATE INDEX idx_words_language ON words(language_code);
CREATE INDEX idx_words_category ON words(category);
CREATE INDEX idx_words_wordpack ON words(wordpack);
CREATE INDEX idx_relations_type ON words_relations(relation_type);
"""