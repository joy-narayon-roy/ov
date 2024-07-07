import os

from bs4 import BeautifulSoup


def validate_html_file(file_path):
    try:
        with open(file_path, 'r') as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, 'html.parser')
            return (soup.find("body").text.__len__() > 50)
    except Exception as e:
        # Handle any exceptions (e.g., invalid HTML)
        print(f"Error validating HTML: {e}")
        return False


def get_files_list(pth="./log"):
    if os.path.exists(pth):
        return os.listdir(pth)
    return []


def files_regs(arr=[]):
    def map_def(n: str):
        return int(n.split(".")[0])
    return list(map(map_def, arr))


def main(logs_path="./log", htmls_path="./html"):
    print("-"*10, "Remove Invalid log", "-"*10)
    # logs_path = "./log"
    # htmls_path = "./html"
    logs_regs = files_regs(get_files_list(logs_path))
    htmls_regs = files_regs(get_files_list(htmls_path))
    for log_reg in logs_regs:
        if (log_reg in htmls_regs):
            is_html_valid = validate_html_file(f"{htmls_path}/{log_reg}.html")
            if is_html_valid:
                print(f"{logs_path}/{log_reg}.log is Invalid.")
                os.remove(f"{logs_path}/{log_reg}.log")

    print("Old logs :", logs_regs.__len__())
    print("Now Logs :", get_files_list(logs_path).__len__())
    print("-"*10, "Done Remving Invalid log", "-"*10)


if __name__ == "__main__":
    main()
