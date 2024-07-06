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
            print()
            print(http_err)
            print(http_err.request.path_url)
            print(http_err.request.url)
            print(http_err.errno)
            print(http_err.args)
            print()
            print(dir(http_err))
            print(type(http_err))
            print()
            break
        except Exception as err:
            print()
            print(err)
            print(type(err))
            print(dir(err))
            print()
            # if not reg:
            #     print(err, "\n", reg)
            #     exit()
            logger(reg, str(err))
            print(err, "\n", reg)
            exit()


if __name__ == "__main__":
    worker()
