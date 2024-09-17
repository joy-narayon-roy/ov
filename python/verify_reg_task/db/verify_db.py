import sqlite3

COUNT_TABLE = '''
CREATE TABLE IF NOT EXISTS "Count" (
	"id"	INTEGER NOT NULL UNIQUE,
	"curr"	INTEGER NOT NULL DEFAULT 22225266100,
	PRIMARY KEY("id" AUTOINCREMENT)
);
'''
VALID_TABLE = '''
CREATE TABLE IF NOT EXISTS "Valid" (
	"reg"	INTEGER NOT NULL UNIQUE,
	"checked"	BOOLEAN DEFAULT 1,
	"valid"	BOOLEAN DEFAULT 1,
	"raw_data"	JSON DEFAULT '{}',
	PRIMARY KEY("reg")
);
'''

FAILD_COUNT_TABLE = '''
CREATE TABLE IF NOT EXISTS "Failed" (
	"reg"	INTEGER NOT NULL UNIQUE,
	"checked"	BOOLEAN DEFAULT 0,
	PRIMARY KEY("reg")
);
'''

DEFAULT_COUNT = '''
INSERT OR IGNORE INTO Count(id,curr) VALUES (1,22221000000)
'''


def use_db(pth: str) -> sqlite3.Connection:
    conn = sqlite3.connect(pth, 60, check_same_thread=False)
    conn.execute(COUNT_TABLE)
    conn.execute(VALID_TABLE)
    conn.execute(FAILD_COUNT_TABLE)
    conn.execute(DEFAULT_COUNT)
    conn.commit()
    return conn
