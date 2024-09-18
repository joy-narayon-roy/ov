import sqlite3
import traceback

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


def remove_valid_from_failed(conn: sqlite3.Connection):
    try:
        print("\t\tWTF remove_valid_from_failed")

        # Corrected SQL query with parentheses around the subquery
        conn.execute("""
            DELETE FROM Failed
            WHERE reg IN (SELECT reg FROM Valid);
        """)
        # Commit the changes to the database
        conn.commit()
        print("\t\tWTF backing remove_valid_from_failed")

    except sqlite3.Error as e:
        # Roll back any changes if there is an error
        conn.rollback()
        print(f"An error occurred: {e}")


def move_data_from_selected_to_failed(conn: sqlite3.Connection):
    cursor = conn.cursor()

    try:
        print("\tWTF move_data_from_selected_to_failed")

        cursor.execute("""
            INSERT OR IGNORE INTO Failed (reg, checked)
            SELECT reg, checked FROM Selected;
        """)

        cursor.execute("DELETE FROM Selected;")
        conn.commit()
        remove_valid_from_failed(conn)
        print("\tWTF Back move_data_from_selected_to_failed")

    except sqlite3.Error as e:
        conn.rollback()
        print(f"An error occurred: {e}")

    # finally:
    #     conn.close()


def use_db(pth: str) -> sqlite3.Connection:
    conn = sqlite3.connect(pth, 300, check_same_thread=False)
    conn.execute(COUNT_TABLE)
    conn.execute(SELECTED_TABLE)
    conn.execute(VALID_TABLE)
    conn.execute(FAILD_COUNT_TABLE)
    conn.execute(DEFAULT_COUNT)
    conn.commit()
    print("WTF use_db")
    move_data_from_selected_to_failed(conn)
    print("WTF Back use_db")
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
        traceback.print_exc()
        print('-'*20, "--------", '-'*20)
        conn.rollback()
        return None


def processes_successs(conn: sqlite3.Connection, reg, *, commit=True):
    conn.execute("DELETE FROM Selected WHERE reg = (?);", (reg,))
    if commit:
        conn.commit()


def get_valid_regs(conn: sqlite3.Connection):
    curs = conn.execute("SELECT reg FROM Valid;")
    results = curs.fetchall()
    results = list(map(lambda x: x[0], results))
    return results


def get_failed_reg(conn: sqlite3.Connection):
    try:
        # Start an immediate transaction to lock the table
        conn.execute("BEGIN IMMEDIATE;")
        cursor = conn.execute(
            "SELECT reg FROM Failed LIMIT 1;")
        failed_reg = cursor.fetchone()

        if not failed_reg:
            return None

        failed_reg = failed_reg[0]
        if failed_reg:
            conn.execute(
                "DELETE FROM Failed WHERE reg = ?;", (failed_reg,))
            conn.execute(
                "INSERT OR IGNORE INTO Selected(reg) VALUES (?);", (failed_reg,))
            conn.commit()
            return failed_reg
        else:
            conn.rollback()  # Rollback if no URL was found
            return None
    except sqlite3.Error as e:
        print('-'*20, "DB Error", '-'*20)
        print(e)
        traceback.print_exc()
        print('-'*20, "--------", '-'*20)
        conn.rollback()
        return None


if __name__ == "__main__":
    use_db("./db/verify_task.db")
