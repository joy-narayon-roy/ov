import sqlite3


def stop():
    conn = sqlite3.connect("./db/verify_task.db",
                           timeout=60, check_same_thread=False)
    curs = conn.execute("SELECT id,end FROM Count;")
    counts = curs.fetchall()
    for count in counts:
        (id, end) = count
        conn.execute("UPDATE Count SET end = ? WHERE id = ?", (0, id))
    conn.commit()
    inp = input("Press enter when all programs stoped.")
    for count in counts:
        (id, end) = count
        conn.execute("UPDATE Count SET end = ? WHERE id = ?", (end, id))
    conn.commit()
    return


if __name__ == "__main__":
    stop()
