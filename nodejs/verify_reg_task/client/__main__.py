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
    res = req.get(f'http://localhost:{MASTER_PORT}/v/t/next')
    res.raise_for_status()
    return res.json()['reg']


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
        except req.exceptions.HTTPError as http_err:
            if(http_err.request.url == "http://localhost:8100/v/t/next"):
                print("Master server error")
                print(err)
                exit()
            print(reg, http_err)
            logger(reg, str(http_err))
            break
        except Exception as err:
            logger(reg, str(err))
            print(err, "\n", reg)
            exit()


if __name__ == "__main__":
    worker()
