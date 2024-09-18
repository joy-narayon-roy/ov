import requests as req
import sqlite3
import db_helper as db_helper
import json
import os
from bs4 import BeautifulSoup

COUNT_ID = 1


def logger(reg, data=""):
    if not os.path.exists("./log"):
        os.mkdir("./log")
    f = open(f'./log/{reg}.log', "w")
    f.write(f'{reg} : {data}')
    f.close()


def save_as_json(name, data):
    if not os.path.exists("./data"):
        os.mkdir("./data")
    file = open(f"./data/{name}.json", "w")
    file.write(json.dumps(data, indent=4))
    file.close()
    return


def delete_file(pth):
    if os.path.exists(pth):
        os.remove(pth)
    return


def get_reg(conn: sqlite3.Connection) -> int | None:
    return db_helper.get_counter_current(conn)


def verify(reg):
    try:
        # TODO:
        res = req.post(
            "http://45.64.132.251:80/verification.php", {"reg": reg})
        res.raise_for_status()
        if not os.path.exists("./html"):
            os.mkdir("./html")
        file = open(f'./html/{reg}.html', 'w')
        file.write(res.text)
        file.close()
        return (f'{res.content}'.find("<table>") > 0, res.text)
    except Exception as err:
        print(err, reg)
        logger(reg, str(err))
        exit()


def read_html(reg, html_res):
    data_obj = {}
    html_file = BeautifulSoup(html_res, "html.parser")

    table = html_file.find('table')
    if not table:
        return None
    for row in table.find_all('tr'):  # type: ignore
        [col1, col2] = row.find_all('td')
        data_obj[col1.text] = col2.text
    # type: ignore
    data_obj["img"] = f"{html_file.find('img').attrs.get('src')}"

    save_as_json(reg, data_obj)
    return data_obj


def this_is_valid(conn: sqlite3.Connection, reg: int, data: dict):
    reg = int(reg)
    conn.execute(f'INSERT OR IGNORE INTO Valid(reg,raw_data) VALUES (?,?)',
                 (reg, json.dumps(data)))
    conn.commit()
    return reg


def worker(worker_id=1):
    print("Worker ", worker_id)
    db_conn = db_helper.use_db("./db/verify_task.db")
    print("Worker ", worker_id)
    while True:
        print("Worker ", worker_id)
        try:
            # TODO:
            # reg = "22225266100" or get_reg()  # Test
            reg = get_reg(db_conn)
            if not reg:
                print("No reg found")
                exit()

            print(reg)

            (exist, html_res) = verify(reg)
            if exist:
                raw_data = read_html(reg, html_res)
                this_is_valid(db_conn, reg, raw_data)
                print(f"{worker_id}. {reg} Exist")
            else:
                print(f"{worker_id}. {reg} Not Exist")

            db_helper.processes_successs(db_conn, reg)
            delete_file(f'./html/{reg}.html')
            delete_file(f'./log/{reg}.log')
            delete_file(f'./data/{reg}.json')
        except KeyboardInterrupt:
            logger(reg, f"{reg} : Exit")
            db_conn.commit()
            print(f"{worker_id}.", reg, "Exit")
            exit()
        except Exception as err:
            logger(reg, str(err))
            db_conn.commit()
            print(err, "\n", f"{worker_id}.", reg)
            exit()
        # break


def failed_worker():
    conn = db_helper.use_db("./db/verify_task.db")
    stop = False
    while not stop:
        try:
            reg = db_helper.get_failed_reg(conn)
            if not reg:
                stop = True
                break

            (exist, html_res) = verify(reg)
            if exist:
                raw_data = read_html(reg, html_res)
                this_is_valid(conn, reg, raw_data)
                print(f"{0}. {reg} Exist")
            else:
                print(f"{0}. {reg} Not Exist")

            db_helper.processes_successs(conn, reg)
            delete_file(f'./html/{reg}.html')
            delete_file(f'./log/{reg}.log')
            delete_file(f'./data/{reg}.json')

        except Exception as err:
            logger(reg, str(err))
            conn.commit()
            print(err, '\n', reg)
            exit()
            return 0
        conn.commit()
        conn.close()


if __name__ == "__main__":
    failed_worker()
    print("Start Main Work")
    worker()
    # conn = db_helper.use_db("./test.db")
    # curr = 22221000004 or db_helper.get_counter_current(conn)
    # db_helper.processes_successs(conn, curr)
    # print(curr)
    # test()
