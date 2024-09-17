import sqlite3

COUNT_TABLE = '''
CREATE TABLE IF NOT EXISTS "Count" (
	"id"	INTEGER NOT NULL UNIQUE,
	"start" INTEGER NOT NULL DEFAULT 22210000000,
	"curr"	INTEGER NOT NULL DEFAULT 22210000000,
	"end"	INTEGER NOT NULL DEFAULT 23000000000,
	PRIMARY KEY("id" AUTOINCREMENT)
);
'''

SELECTED_TABLE = '''
CREATE TABLE IF NOT EXISTS "Selected" (
	"reg"	INTEGER NOT NULL UNIQUE,
	"checked"	BOOLEAN DEFAULT 0,
	PRIMARY KEY("reg")
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
    conn.execute(SELECTED_TABLE)
    conn.execute(VALID_TABLE)
    conn.execute(FAILD_COUNT_TABLE)
    conn.execute(DEFAULT_COUNT)
    conn.commit()
    return conn


def get_counter_current(conn: sqlite3.Connection, *, counter_id=1) -> int | None:
    try:
        # Start an immediate transaction to lock the table
        conn.execute("BEGIN IMMEDIATE;")
        cursor = conn.execute(
            "SELECT curr,end FROM Count WHERE id = ? LIMIT 1;", (counter_id,))
        counter = cursor.fetchone()

        if counter:
            (curr, end) = counter
            curr += 1
            if curr > end:
                return None
            conn.execute(
                "UPDATE Count SET curr = ? WHERE id = ?;", (curr, 1))
            conn.execute(
                "INSERT OR IGNORE INTO Selected(reg) VALUES (?);", (curr,))
            conn.commit()
            return curr
        else:
            conn.rollback()  # Rollback if no URL was found
            return None
    except sqlite3.Error as e:
        print('-'*20, "DB Error", '-'*20)
        print(e)
        print('-'*20, "--------", '-'*20)
        conn.rollback()
        return None


def processes_successs(conn: sqlite3.Connection, reg, *, commit=True):
    conn.execute("DELETE FROM Selected WHERE reg = (?);", (reg,))
    if commit:
        conn.commit()

if __name__ =="__main__":
    use_db("./db/verify_task.db")