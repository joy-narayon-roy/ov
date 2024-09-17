import requests as req
import sqlite3
import db.verify_db as verify_db
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


def get_reg(conn: sqlite3.Connection) -> int | None:
    try:
        # Start an immediate transaction to lock the table
        conn.execute("BEGIN IMMEDIATE;")
        cursor = conn.execute(
            "SELECT curr FROM Count WHERE id = ? LIMIT 1;",(COUNT_ID,))
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
    db_conn = verify_db.use_db("./db/verify_task.db")
    while True:
        try:
            # TODO:
            # reg = "22225266100" or get_reg()  # Test
            reg = get_reg(db_conn)
            if not reg:
                print("No reg found")
                exit()

            (exist, html_res) = verify(reg)
            if exist:
                raw_data = read_html(reg, html_res)
                this_is_valid(db_conn, reg, raw_data)
                print(f"{worker_id}. {reg} Exist\n")
            else:
                print(f"{worker_id}. {reg} Not Exist\n")

        except KeyboardInterrupt:
            logger(reg, f"{reg} : Exit")
            print(f"\n{worker_id}.", reg, "Exit")
            exit()
        except Exception as err:
            logger(reg, str(err))
            print(err, "\n", f"{worker_id}.", reg)
            exit()
        break


if __name__ == "__main__":
    worker()
    # test()
