import requests as req
import time


def get_reg():
    try:
        res = req.get("http://localhost:8001")
        res.raise_for_status()
        return res.text
    except Exception as err:
        print(err)
        exit()


def main():
    for i in range(5):
        start_t = time.time()
        get_reg()
        end_t = time.time()
        print(i, end_t-start_t)

main()