import sqlite3


def main():
    verify_db_conn = sqlite3.connect(
        "./db/verify_task.db", 60, cached_statements=False)
    valid_regs = verify_db_conn.execute("SELECT reg FROM Valid").fetchall()

    reg_db_conn = sqlite3.connect(
        "../data_collected/db/regs.db", 60, check_same_thread=False)
    reg_db_conn.executemany(
        'INSERT OR IGNORE INTO Regs(reg,collected) VALUES (?,0)', valid_regs)
    reg_db_conn.commit()

    return 0


if __name__ == "__main__":
    main()
