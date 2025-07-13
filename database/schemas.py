# Paste your schema as a single string
schema = """
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS LexicalEntry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lexeme VARCHAR(50) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Translation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lexeme VARCHAR(50) NOT NULL,
    category VARCHAR(20),
    wordpack VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS EntryTranslation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_id INTEGER NOT NULL,
    translation_id INTEGER NOT NULL,
    FOREIGN KEY (entry_id) REFERENCES LexicalEntry(id) ON DELETE CASCADE,
    FOREIGN KEY (translation_id) REFERENCES Translation(id) ON DELETE CASCADE,
    UNIQUE(entry_id, translation_id)
);
"""