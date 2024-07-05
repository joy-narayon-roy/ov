import requests as req

MASTER_PORT = 8100


def verify(reg):
    try:
        res = req.post(
            "http://regicard.nu.edu.bd/verification.php", {"reg": reg})
        # if res.status_code > 250:
        #     logger(reg)
        res.raise_for_status()
        file = open(f'./html/{reg}.html', 'w')
        file.write(res.text)
        file.close()
        return f'{res.content}'.find("<table>") > 0
    except Exception as err:
        print(err)
        logger(reg, str(err))
        exit()


def logger(reg, data=""):
    f = open(f'./log/{reg}.log')
    f.write(f'{reg} : {data}')
    f.close()


def get_reg():
    res = req.get(f'http://localhost:{MASTER_PORT}/v/t/next')
    res.raise_for_status()
    return res.json()['reg']


def this_is_valid(reg):
    res = req.get(f'http://localhost:{MASTER_PORT}/v/{reg}')
    res.raise_for_status()


def worker():
    while True:
        reg = get_reg()
        exist = verify(reg)
        if exist:
            this_is_valid(reg)
            print(reg, "Exist")
        else:
            print(reg, "Not exist")
        # break


if __name__ == "__main__":
    try:
        worker()
    except KeyboardInterrupt:
        exit()
    except Exception as err:
        print(err)
