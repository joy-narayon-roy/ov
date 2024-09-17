import sqlite3
import requests as req
import time
import traceback


def old_get_reg() -> int:
    conn = sqlite3.connect("./test.db")
    curs = conn.cursor()
    curr = curs.execute(
        '''SELECT curr FROM Count WHERE id = 1''').fetchone()[0]+1
    curs.execute('UPDATE Count SET curr = ? WHERE id = 1', (curr,))
    conn.commit()
    conn.close()
    return curr


def get_reg() -> int | None:
    try:
        conn = sqlite3.connect("./test.db",
                               60, check_same_thread=False)
        # Start an immediate transaction to lock the table
        conn.execute("BEGIN IMMEDIATE;")
        cursor = conn.execute(
            "SELECT curr FROM Count WHERE id = 1 LIMIT 1;")
        curr = cursor.fetchone()

        if curr:
            curr = curr[0]
            curr += 1
            conn.execute(
                "UPDATE Count SET curr = ? WHERE id = ?;", (curr, 1))
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


def check_valid(reg):
    res = req.get(f'http://127.0.0.1/valid/{reg}')
    res.raise_for_status()
    return True


def worker():
    while True:
        try:
            reg = get_reg()
            if not reg:
                break
            valid = check_valid(reg)
            if valid:
                print(reg, "Valid")
                # time.sleep(0.8)
        except KeyboardInterrupt:
            break
        except Exception as err:
            print('-'*20, "Error", '-'*20)
            print(err)
            # print(reg, "Not valid")
            print('-'*20, "-----", '-'*20)
            traceback.print_exc()
            break


def test():
    print("Test")
    reg = get_reg()
    print(reg)


def main():
    worker()
    # test()


if __name__ == "__main__":
    main()
