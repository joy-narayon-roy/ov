import requests as req
import concurrent.futures
from sqlite3 import connect

conn = connect("./db/regs.db", timeout=3600, check_same_thread=False)
cursor = conn.cursor()

LIMIT = 20

def get_img(url):
    res = req.get(url)
    res.raise_for_status()
    print(url, "Collected.")
    return (res.content, url)


def get_img_urls(limit=10):
    urls = cursor.execute(
        f"SELECT img_url FROM Valid_students WHERE img IS NULL LIMIT {limit}").fetchall()
    urls = list(map(lambda d: d[0], urls))
    return urls


def collect_url_datas(url_list):
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=LIMIT) as executor:
            while True:
                results = list(executor.map(get_img, url_list))
                return results
    except Exception as err:
        print(err)
        exit()


def main():
    while True:
        try:
            urls = get_img_urls(limit=LIMIT)

            if urls.__len__() == 0:
                break

            datas = collect_url_datas(urls)
            cursor.executemany(
                f"UPDATE OR IGNORE Valid_students SET img = ? WHERE img_url = ?", datas)
            conn.commit()
            print(datas.__len__(), "Saved")

            # break
        except KeyboardInterrupt:
            exit()
        except Exception as err:
            print(err)
            exit()


if __name__ == "__main__":
    main()
