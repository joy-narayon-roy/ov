import sqlite3
import time
import requests as req
import sys

TEST_DB_PATH = "./db/test.db"
DB_PATH = "./db/ov_reg_rendom.db"
START_REG = 22225000000
END_REG = 22226000000

# Increase the timeout to 30 seconds
conn = sqlite3.connect(DB_PATH, timeout=30)
cursor = conn.cursor()


def printf(print_str):
    sys.stdout.write(f"{print_str}")
    sys.stdout.flush()


def verify(reg):
    try:
        res = req.post(
            "http://45.64.132.251:80/verification.php", {"reg": reg})
        res.raise_for_status()
        with open(f'./html/{reg}.html', 'w') as file:
            file.write(res.text)
        return f'{res.content}'.find("<table>") > 0
    except Exception as err:
        print(err, reg)
        logger(reg, str(err))
        exit()


def logger(reg, data=""):
    with open(f'./log/{reg}.log', "w") as f:
        f.write(f'{reg} : {str(data)}')


def get_reg():
    retry_count = 5
    for _ in range(retry_count):
        try:
            ALL_QUERY = '''SELECT reg FROM Regs WHERE checked=0 LIMIT 1'''
            SUB_QURY = f'''SELECT reg FROM Regs WHERE reg>= {START_REG} AND reg < {END_REG} AND checked=0 LIMIT 1'''
            reg = cursor.execute(SUB_QURY).fetchone()
            if not reg:
                return None
            reg = int(reg[0])
            cursor.execute(
                '''UPDATE Regs SET checked = ? WHERE reg = ?''', (True, reg))
            conn.commit()
            return reg
        except sqlite3.OperationalError as e:
            print(f"Database is locked, retrying in a moment... {e}")
            time.sleep(2)  # Sleep for 2 seconds before retrying
    print("Failed to get reg after retries.")
    return None


def this_is_valid(reg):
    retry_count = 5
    for _ in range(retry_count):
        try:
            cursor.execute(
                '''UPDATE Regs SET valid = ? WHERE reg = ?''', (True, reg))
            conn.commit()
            return
        except sqlite3.OperationalError as e:
            print(f"Database is locked, retrying in a moment... {e}")
            time.sleep(2)  # Sleep for 2 seconds before retrying
    print(f"Failed to mark {reg} as valid after retries.")


def worker():
    while True:
        try:
            reg = get_reg()
            if not reg:
                print("All Done.")
                return "Done"
            printf(str(reg))
            exist = verify(reg)
            if exist:
                this_is_valid(reg)
                printf(" Exist\n")
            else:
                printf(" Not Exist\n")
        except KeyboardInterrupt:
            print(reg, "Exit")
            logger(reg, "Exit")
            conn.commit()
            conn.close()
            exit()


if __name__ == "__main__":
    worker()
