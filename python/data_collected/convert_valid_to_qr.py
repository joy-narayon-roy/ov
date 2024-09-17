import sqlite3
conn = sqlite3.connect("./db/regs.db", timeout=60, check_same_thread=False)
curs = conn.cursor()


def main():
    pass

if __name__ == "__main__":
    main()