import threading
import requests
import sqlite3
import os

'''
CREATE TABLE "Files" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"file_data"	BLOB NOT NULL,
	"path"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
)
'''


def fetch_data(name, fp):
    file_path = f"{fp}/{name}"
    with open(file_path, "r") as file:
        data = file.read()
        file.close()
        return (name, data, file_path)


def split_array(arr, size):
    return [arr[i:i+size] for i in range(0, len(arr), size)]


def read_and_save_db(files: list, path="./"):
    threads = []
    results = []
    conn = sqlite3.connect("./files_ov.db")
    curs = conn.cursor()
    curs.execute('''
    CREATE TABLE IF NOT EXISTS "Files" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"file_data"	BLOB NOT NULL,
	"path"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
    )
    ''')

    def fetch_data_thread(name, fp):
        result = fetch_data(name, fp)
        results.append(result)

    # Create and start threads for each URL
    for file in files:
        thread = threading.Thread(target=fetch_data_thread, args=(file, path))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    try:
        curs.executemany('''
        INSERT INTO Files (name, file_data, path) VALUES ( ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
        name=excluded.name,
        file_data=excluded.file_data,
        path=excluded.path''', results)
    except Exception as err:
        print(err)
        exit()
    print(results.__len__(),"Saved")

    conn.commit()
    conn.close()


def main():
    foler_path = "./html"
    htmls = os.listdir(foler_path)
    htmls = split_array(htmls, 1000)
    for html in htmls:
        read_and_save_db(html, foler_path)
        break


if __name__ == "__main__":
    main()
