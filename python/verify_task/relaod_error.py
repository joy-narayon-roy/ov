import os
import sqlite3

TEST_DB_PATH = "./db/test.db"
DB_PATH = "./db/ov_reg_rendom.db"
# DB_PATH = TEST_DB_PATH

def map_def(name):
    return int(name.split(".")[0])


def main():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    logs = os.listdir("./log")
    logs = list(map(map_def, logs))
    logs.sort()
    for err_reg in logs:
        exist = cursor.execute(
            f'SELECT * FROM Regs WHERE reg={err_reg}').fetchone()
        if not exist:
            cursor.execute(
                '''INSERT INTO Regs (reg,checked,valid) VALUES (?,?,?)''', (err_reg, False, False))
            print(err_reg, "Reloaded")
        else:
            cursor.execute(
                '''UPDATE Regs SET checked = ? WHERE reg = ?''', (False, err_reg))
            print(err_reg, "Checked Updated")
        # break
    conn.commit()


if __name__ == "__main__":
    main()
