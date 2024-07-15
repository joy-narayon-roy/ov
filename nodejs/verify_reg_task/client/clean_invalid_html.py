import os
from bs4 import BeautifulSoup
import json


def convert_to_key(key):
    return str(key).replace("'", "").replace(" ", "_").replace(":", "")


def save_as_json(name, data):
    file = open(f"./data/{name}.json", "w")
    file.write(json.dumps(data, indent=4))
    file.close()


def read_html(file_path):
    file_name = os.path.split(file_path)[1].split(".")[0]
    file = open(file_path)
    data_obj = {}
    html_file = BeautifulSoup(file.read(), "html.parser")

    table = html_file.find('table')
    if not table:
        # print("Not valid")
        return 0

    for row in table.find_all('tr'):
        [col1, col2] = row.find_all('td')
        data_obj[col1.text] = col2.text

    data_obj["img"] = f"{html_file.find('img').attrs.get('src')}"

    save_as_json(file_name, data_obj)
    print("\t", file_name, "Saved")
    return 1


def main(pth="./html"):
    i = 1
    files = os.listdir(pth)
    file_len = files.__len__()
    for file in files:
        file_path = f"{pth}/{file}"
        data_exist = read_html(file_path)
        os.remove(file_path)
        percentage = (i / file_len) * 100
        percentage_str = "{:.2f}".format(percentage)
        if not data_exist:
            print(f"{percentage_str}% Need to delete", file_path)
        else:
            print(f"{percentage_str}% Exist", file_path)
        i += 1
        # break


if __name__ == "__main__":
    main()
# read_html("./demo_valid.html")
