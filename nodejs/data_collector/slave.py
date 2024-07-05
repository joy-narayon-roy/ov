import requests as req
from time import sleep
import json

MASTER = "http://localhost:5000"
SERVER_ADDRESS = "http://103.113.200.45:8006/api/student/login"


def et_data():
    file = open("./data/slave-22225266100.json")
    data = (file.read())
    file.close()
    return data


def server_ok():
    try:
        res = req.get(f'{MASTER}/ok')
        res.raise_for_status()
        return res.json()["state"]
    except Exception as err:
        return False


def get_reg():
    try:
        res = req.get(f'{MASTER}/c/n')
        res.raise_for_status()
        return res.text
    except Exception:
        exit()


def get_reg_data(reg):
    try:
        # TODO: Remove return
        # return et_data()
        form_data = {
            "username": str(reg),
            "password": "123456",
            "recaptcha-v3": "undefined"
        }

        res = req.post(SERVER_ADDRESS, data=form_data, timeout=3600)
        file = open(f'./data/slave-{reg}.json', 'w')
        file.write(res.text)
        file.close()
        res.raise_for_status()
        return res.text
    except Exception as err:
        print(err)
        exit()


def send_to_master(reg, index, data):
    try:
        res = req.post(f'{MASTER}/v/{reg}/{index}', data={"data": data})
        res.raise_for_status()
        # print(res.text)
    except Exception as err:
        print(err)
        exit()


def worker():
    print("I am worker")
    while True:
        reg_info = get_reg()
        [reg, index] = reg_info.split(",")
        # TODO: Replace 22225266100 to reg
        reg_data = get_reg_data(reg)
        send_to_master(reg, index, reg_data)
        print(reg, "Collected")
        # break


def main():
    while True:
        ok = server_ok()
        if ok:
            print("Master Ok...")
            worker()
            break
        else:
            print("Master not ok. Going to sleep 10s")
            sleep(10)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit()
