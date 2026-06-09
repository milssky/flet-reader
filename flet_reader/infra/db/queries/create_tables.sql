PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    language TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS book_authors (
    book_id INTEGER NOT NULL,
    order_index INTEGER NOT NULL,
    name TEXT NOT NULL,

    PRIMARY KEY (book_id, order_index),
    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS chapters (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    parent_id INTEGER,
    title TEXT,
    order_index INTEGER NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,

    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
    FOREIGN KEY (parent_id) REFERENCES chapters (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS blocks (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    chapter_id INTEGER NOT NULL,
    order_index INTEGER NOT NULL,
    type TEXT NOT NULL,
    content TEXT,
    payload BLOB,

    FOREIGN KEY (book_id) REFERENCES books (id) ON DELETE CASCADE,
    FOREIGN KEY (chapter_id) REFERENCES chapters (id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_chapters_book_order
ON chapters (book_id, order_index);

CREATE INDEX IF NOT EXISTS idx_blocks_chapter_order
ON blocks (chapter_id, order_index);
