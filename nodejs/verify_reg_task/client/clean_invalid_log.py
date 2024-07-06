import os


def get_files_list(pth="./log"):
    if os.path.exists(pth):
        return os.listdir(pth)
    return []


def files_regs(arr=[]):
    def map_def(n: str):
        return int(n.split(".")[0])
    return list(map(map_def, arr))


def main():
    logs_path = "./log"
    htmls_path = "./html"
    logs_regs = files_regs(get_files_list(logs_path))
    htmls_regs = files_regs(get_files_list(htmls_path))
    for log_reg in logs_regs:
        if (log_reg in htmls_regs):
            print(f"{logs_path}/{log_reg}.log   Invalid")
            break
        print(log_reg, log_reg in htmls_regs)
    

    print(logs_regs.__len__())
    print(htmls_regs.__len__())


if __name__ == "__main__":
    main()
