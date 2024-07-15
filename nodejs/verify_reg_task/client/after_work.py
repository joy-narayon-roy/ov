import os
import requests as req

MASTER_PORT = 8100


def get_htmls(pth):
    files = os.listdir(pth)
    return list(filter(lambda d: d.split(".")[1] == "html", files))


def handel_logs(pth):
    files = os.listdir(pth)
    print("-"*20, "Log started", "-"*20)
    logs = list(filter(lambda f: f.split(".")[1] == "log", files))
    log_regs = list(map(lambda lf: int(lf.split(".")[0]), logs))
    print("Logs found", log_regs.__len__())
    res = req.post(f"http://localhost:{MASTER_PORT}/v/reload", json=log_regs)
    res.raise_for_status()
    res_log_reg = res.json()
    for res_log in res_log_reg:
        os.remove(f'./log/{res_log}.log')
        print(res_log, "Remove")

    print("-"*20, "Log Done", "-"*20)


def main():
    HTML_DIR = "./html"
    LOGS_DIR = "./log"
    handel_logs(LOGS_DIR)

    # print(get_htmls(HTML_DIR).__len__())


if __name__ == "__main__":
    main()
