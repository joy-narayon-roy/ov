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
    except KeyboardInterrupt:
        conn.commit()
        conn.close()
        exit()
    except Exception as err:
        conn.commit()
        conn.close()
        print(err)
        exit()
    print(results.__len__(), "Saved")

    conn.commit()
    conn.close()


def main():
    foler_path = "./html"
    fector = int(input("Enter at a time (default : 1000)")) or 1000
    htmls = os.listdir(foler_path)
    total_files = htmls.__len__()
    print("Total files :", total_files)
    htmls = split_array(htmls, fector)
    count = 1
    for html in htmls:
        read_and_save_db(html, foler_path)
        persentage = "{:.2f}".format(((count)/htmls.__len__()) * 100)
        persentage = f"{persentage}%"
        print(persentage, "Done")
        count += 1
        # break


if __name__ == "__main__":
    main()
