import requests as req
import sys
import json
import os
from bs4 import BeautifulSoup

MASTER_PORT = 8100


def printf(stri):
    sys.stdout.write(f"{stri}")
    sys.stdout.flush()


def logger(reg, data=""):
    f = open(f'./log/{reg}.log', "w")
    f.write(f'{reg} : {data}')
    f.close()


def save_as_json(name, data):
    file = open(f"./data/{name}.json", "w")
    file.write(json.dumps(data, indent=4))
    file.close()


def get_reg():
    try:
        res = req.get(f'http://localhost:{MASTER_PORT}/v/t/next')
        res.raise_for_status()
        return res.json()['reg']
    except Exception as err:
        print(err)
        exit()


def verify(reg):
    try:
        # TODO:
        res = req.post(
            "http://45.64.132.251:80/verification.php", {"reg": reg})
        res.raise_for_status()
        file = open(f'./html/{reg}.html', 'w')
        file.write(res.text)
        file.close()
        return [f'{res.content}'.find("<table>") > 0, res.text]
    except Exception as err:
        print(err, reg)
        logger(reg, str(err))
        exit()


def read_html(reg, html_res):
    data_obj = {}
    html_file = BeautifulSoup(html_res, "html.parser")

    table = html_file.find('table')
    if not table:
        return None
    for row in table.find_all('tr'): # type: ignore
        [col1, col2] = row.find_all('td')
        data_obj[col1.text] = col2.text
    data_obj["img"] = f"{html_file.find('img').attrs.get('src')}" # type: ignore

    save_as_json(reg, data_obj)
    return data_obj


def this_is_valid(reg, data={}):
    res = req.post(f'http://localhost:{MASTER_PORT}/v/{reg}', json=data)
    res.raise_for_status()


def worker(worker_id=1):
    while True:
        try:
            # TODO:
            # reg = "22225266100" or get_reg() #Test
            reg = get_reg()
            printf(f"{worker_id}. {reg}")

            [exist, html_res] = verify(reg)
            if exist:
                raw_data = read_html(reg, html_res)
                this_is_valid(reg, raw_data)
                printf(" Exist\n")
            else:
                printf(" Not Exist\n")

        except KeyboardInterrupt:
            logger(reg, f"{reg} : Exit")
            print(f"\n{worker_id}.", reg, "Exit")
            exit()
        except Exception as err:
            logger(reg, str(err))
            print(err, "\n", f"{worker_id}.", reg)
            exit()


if __name__ == "__main__":
    worker()
