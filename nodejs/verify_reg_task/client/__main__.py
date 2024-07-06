import requests as req
import sys

MASTER_PORT = 8100


def printf(stri):
    sys.stdout.write(f"{stri}")
    sys.stdout.flush()


def verify(reg):
    try:
        # res = req.post(
        #    "http://regicard.nu.edu.bd/verification.php", {"reg": reg})
        res = req.post(
            "http://45.64.132.251:80/verification.php", {"reg": reg})
        res.raise_for_status()
        file = open(f'./html/{reg}.html', 'w')
        file.write(res.text)
        file.close()
        return f'{res.content}'.find("<table>") > 0
    except Exception as err:
        print(err, reg)
        logger(reg, str(err))
        exit()


def logger(reg, data=""):
    f = open(f'./log/{reg}.log', "w")
    f.write(f'{reg} : {data}')
    f.close()


def get_reg():
    try:
        res = req.get(f'http://localhost:{MASTER_PORT}/v/t/next')
        res.raise_for_status()
        return res.json()['reg']
    except Exception as err:
        print(err)
        exit()


def this_is_valid(reg):
    res = req.get(f'http://localhost:{MASTER_PORT}/v/{reg}')
    res.raise_for_status()


def worker():
    while True:
        try:
            reg = get_reg()
            printf(reg)

            exist = verify(reg)
            if exist:
                this_is_valid(reg)
                printf(" Exist\n")
            else:
                printf(" Not Exist\n")

        except KeyboardInterrupt:
            logger(reg, f"{reg} : Exit")
            print(reg, "Exit")
            exit()
        except Exception as err:
            logger(reg, str(err))
            print(err, "\n", reg)
            exit()


if __name__ == "__main__":
    worker()
