import os
import requests as req
import sqlite3
import module as my_mod

MASTER_PORT = 8100


def get_store_db():
    conn = sqlite3.connect("../db/store.db")
    curs = conn.cursor()
    curs.execute('''
    CREATE TABLE IF NOT EXISTS "html" (
	"name"	TEXT NOT NULL UNIQUE,
	"file_data"	TEXT NOT NULL,
	"valid"	BLOB NOT NULL DEFAULT 0,
	PRIMARY KEY("name")
    )
    ''')
    conn.commit()
    return conn


def handel_logs(pth):
    files = os.listdir(pth)
    print("-"*20, "Log started", "-"*20)
    logs = list(filter(lambda f: f.split(".")[1] == "log", files))
    log_regs = list(map(lambda lf: int(lf.split(".")[0]), logs))
    print("Logs found", log_regs.__len__())
    res = req.post(f"http://localhost:{MASTER_PORT}/v/reload", json=log_regs)
    res.raise_for_status()
    res_log_reg = res.json()
    for res_log in res_log_reg:
        os.remove(f'./log/{res_log}.log')
        print(res_log, "Remove")

    print("-"*20, "Log Done", "-"*20)


def copy_html_to_store_db(cp="./html"):
    print("-"*20, f"Copy {cp} -> store.db", "-"*20)
    conn = get_store_db()
    curs = conn.cursor()
    path_files = os.listdir(cp)
    html_files = list(filter(lambda d: str(
        d).split(".")[1] == "html", path_files))
    print(f"Total {cp} files :", html_files.__len__())
    f_count = 1
    for html_file in html_files:
        reg = int(html_file.split(".")[0])
        file_pth = f'{cp}/{html_file}'
        html_txt = open(file_pth, "r").read()
        curs.execute(
            '''INSERT OR IGNORE INTO html (name,file_data) VALUES (?,?)''', (html_file, html_txt))
        conn.commit()
        file_data = curs.execute(
            'SELECT file_data FROM html WHERE name = ?', (html_file,)).fetchone()[0]
        if not html_txt == file_data:
            print(reg, "Not eqal")
            raise f"{reg} Not eqal"
        valid_json = my_mod.import_html_export_json(html_txt, reg)
        if valid_json:
            req.post(
                f'http://localhost:{MASTER_PORT}/v/{reg}', json=valid_json).raise_for_status()
            req.get(
                f'http://localhost:8200/insertreg/{reg}').raise_for_status()
        print(f"{f_count}/{html_files.__len__()} {html_file} Saved.{'valid' if bool(valid_json) else 'Invalid'}")
        os.remove(file_pth)
        f_count += 1
        # break
    print("-"*20, f"Copy {cp} -> store.db Done", "-"*20)


def user_intput(msg="Want to skip?(y/n)"):
    print()
    while True:
        inp = str(input(f"{msg}\t")).lower()
        if not inp in ["y", "n"]:
            continue
        print()
        return inp


def main():
    print("Start servers before doing this")

    inp = user_intput("Reload log regs and clean logs? (y/n)")
    if inp == "y":
        handel_logs("./log")

    inp = user_intput("Copy html -> store.db? (y/n)")
    if inp == "y":
        copy_html_to_store_db()

    inp = user_intput("Copy log -> store/log? (y/n)")
    if inp == "y":
        pass


if __name__ == "__main__":
    main()
    # handel_logs("./log")
    pass
