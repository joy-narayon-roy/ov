import time
import requests as req


def get_reg():
    res = req.get("http://localhost:2000")
    res.raise_for_status()
    return res.text


def main():
    start_time = time.time()
    data = get_reg()
    end_time = time.time()
    rt = "{:.3f}s".format(end_time - start_time)
    print(rt, data)


# print(time.time())
main()
