import os
import shutil
from clean_invalid_html import main as clean_invalid_html
from clean_invalid_log import main as clean_invalid_log


def get_persentage(a, b):
    p = (a/b)*100
    p = '{:.2f}'.format(p)
    return f"{p}%"


def cp_to_store_path(cp, dstp):
    print("-"*10, "Copeing Start", "-"*10)

    if not os.path.exists(cp):
        os.makedirs(cp)
    if not os.path.exists(dstp):
        os.makedirs(dstp, exist_ok=True)

    cp_files = os.listdir(cp)
    old_dstp_files = os.listdir(dstp)

    print(f"Src {cp} :", cp_files.__len__())
    print(f"Destination {dstp} :", old_dstp_files.__len__())
    print()

    count = 1
    for cp_file in cp_files:
        src_path = f'{cp}/{cp_file}'
        dst_path = f'{dstp}/{cp_file}'
        shutil.copy2(src_path, dst_path)
        print(get_persentage(count, cp_files.__len__()), cp_file, "Copied.")
        count += 1
        # break
    print()
    print(f"Src {cp} :", cp_files.__len__())
    print(f"Before {dstp} :", old_dstp_files.__len__())
    print(f"Now {dstp} :", os.listdir(dstp).__len__())
    print(
        "-"*10, f"Coping end ({cp} -> {dstp})", "-"*10, "\n")


# cp_html_to_storeHtml()
def main():
    cp_to_store_path("html", "store/html")
    cp_to_store_path("log", "store/log")
    inp = input("Enter to clean invalid log files(y/n)")
    if inp == "y":
        clean_invalid_log()
    inp = input("Enter to clean invalid HTML files(y/n)")
    if inp == "y":
        clean_invalid_html()


main()
