import requests as req
import sys
import sqlite3

TEST_DB_PATH = "./db/test.db"
# DB_PATH = TEST_DB_PATH
DB_PATH = "./db/ov_reg_rendom.db" 

START_REG = 22225000000
END_REG = 22226000000

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


def printf(print_str):
    sys.stdout.write(f"{print_str}")
    sys.stdout.flush()


def verify(reg):
    try:
        #45.64.132.251:80
        # res = req.post(
        #     "http://regicard.nu.edu.bd/verification.php", {"reg": reg})
        res = req.post(
            "http://45.64.132.251:80/verification.php", {"reg": reg})
        res.raise_for_status()
        file = open(f'./html/{reg}.html', 'w')
        file.write(res.text)
        file.close()
        return f'{res.content}'.find("<table>") > 0
    except Exception as err:
        print(err, reg)
        logger(reg, str(err))
        exit()


def logger(reg, data=""):
    f = open(f'./log/{reg}.log', "w")
    f.write(f'{reg} : {str(data)}')
    f.close()


def get_reg():
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


def this_is_valid(reg):
    cursor.execute('''UPDATE Regs SET valid = ? WHERE reg = ?''',(True, reg))
    conn.commit()


def worker():
    while True:
        try:
            reg = get_reg()
            if not reg:
                print("All Done.")
                return "Done"
            printf(reg)
            exist = verify(reg)
            if exist:
                this_is_valid(reg)
                printf(" Exist\n")
            else:
                printf(" Not Exist\n")
        # break
        except KeyboardInterrupt:
            print(reg, "Exit")
            logger(reg, "Exit")
            conn.commit()
            conn.close()
            exit()


if __name__ == "__main__":
    worker()
    # try:
    #     worker()
    # except KeyboardInterrupt:
    #     exit()
    # except Exception as err:
    #     print(err)
