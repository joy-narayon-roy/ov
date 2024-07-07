import requests as req
import os

MASTER_PORT = 8100


def get_logs_regs(log_path="./log"):
    def map_def(name: str):
        return int(name.split(".")[0])
    logs_files = list(map(map_def, os.listdir("./log")))
    return logs_files


def send_log_reg(reg):
    try:
        res = req.get(f"http://localhost:{MASTER_PORT}/v/reload/{reg}")
        res.raise_for_status()
        return res.json()
    except Exception as err:
        print(err)
        exit()


def main():
    try:
        regs = get_logs_regs()
        for reg in regs:
            sended = send_log_reg(reg)
            print(sended)
            # break
    except KeyboardInterrupt:
        exit()


if __name__ == "__main__":
    main()
