import requests as req
import sys

MASTER_PORT = 8100
curr_reg = None


def printf(stri):
    sys.stdout.write(f"{stri}")
    sys.stdout.flush()


def verify(reg):
    try:
        #res = req.post(
        #    "http://regicard.nu.edu.bd/verification.php", {"reg": reg})
        res = req.post(
            "http://45.64.132.251:80/verification.php", {"reg": reg})
        # if res.status_code > 250:
        #     logger(reg)
        res.raise_for_status()
        file = open(f'./html/{reg}.html', 'w')
        file.write(res.text)
        file.close()
        return f'{res.content}'.find("<table>") > 0
    except Exception as err:
        print(err,reg)
        logger(reg, str(err))
        exit()


def logger(reg, data=""):
    f = open(f'./log/{reg}.log',"w")
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
        #global curr_reg
        reg = get_reg()
        printf(reg)
        curr_reg = reg
        exist = verify(reg)
        if exist:
            this_is_valid(reg)
            #print(reg, "Exist")
            printf(" Exist\n")
        else:
            #print(reg, "Not exist")
            printf(" Not Exist\n")
        curr_reg=f"{curr_reg} Done."
        # break


if __name__ == "__main__":
    try:
        worker()
    except KeyboardInterrupt:
        exit()
    except Exception as err:
        #global curr_reg
        print(err)
        print(curr_reg)
