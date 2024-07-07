from multiprocessing import Process
import requests as req
import time


def get_reg():
    res = req.get(f'http://localhost:{8100}/t/next')
    res.raise_for_status()
    return res.text


def task(name):
    print(name,get_reg())


if __name__ == '__main__':
    processes = []
    for i in range(5):
        p = Process(target=task, args=(i,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
