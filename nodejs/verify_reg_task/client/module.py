import os
import json
from bs4 import BeautifulSoup


def get_persentage(a, b):
    p = (a/b)*100
    p = '{:.2f}'.format(p)
    return f"{p}%"


def save_as_json(name, data, save_path="./data"):
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    file = open(f"{save_path}/{name}.json", "w")
    file.write(json.dumps(data, indent=4))
    file.close()


def import_html_export_json(html_txt, file_name, save_json_pth="./data"):
    data_obj = {}
    html_file = BeautifulSoup(html_txt, "html.parser")

    table = html_file.find('table')
    if not table:
        return None

    for row in table.find_all('tr'):
        [col1, col2] = row.find_all('td')
        data_obj[col1.text] = col2.text

    data_obj["img"] = f"{html_file.find('img').attrs.get('src')}"
    if save_json_pth:
        save_as_json(file_name, data_obj)
    # print("\t", file_name, "Saved")
    return data_obj
