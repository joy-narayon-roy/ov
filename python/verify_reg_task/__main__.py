import db_helper
import os


def remove_valid_html_file(regs: list = []):
    PATH = "./html"
    for reg in regs:
        file_name = f'{PATH}/{reg}.html'
        if not os.path.exists(file_name):
            continue
        os.remove(file_name)
        print(file_name, os.path.exists(file_name))

def move_selected_to_failed():
    print("ok")

def main():
    print("WTF")


def main0():
    conn = db_helper.use_db('./db/verify_task.db')
    curs = conn.execute('SELECT reg FROM Selected')
    result = curs.fetchall()
    result = list(map(lambda x: x[0], result))
    print(result)


if __name__ == "__main__":
    main0()
