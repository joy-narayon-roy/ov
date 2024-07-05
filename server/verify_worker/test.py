import sqlite3


class Config:
    def __init__(self) -> None:
        pass


class DB:
    def __init__(self, db_path) -> None:
        self.__path = db_path
        self.__conn = sqlite3.connect(self.__path)
        self.__cursor = self.__conn.cursor()
        self.__cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT
        )
        ''')
        self.__conn.commit()
        pass


def create_table():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT
    )
    ''')
    conn.commit()
    conn.close()


def insert_data(name, age, email):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (name, age, email) VALUES (?, ?, ?)
    ''', (name, age, email))
    conn.commit()
    conn.close()


def query_data():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    rows = cursor.fetchall()
    conn.close()
    return rows


def update_data(name, new_age):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE users SET age = ? WHERE name = ?
    ''', (new_age, name))
    conn.commit()
    conn.close()


def delete_data(name):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute('''
    DELETE FROM users WHERE name = ?
    ''', (name,))
    conn.commit()
    conn.close()


# Example usage
if __name__ == '__main__':
    create_table()
    insert_data('Alice', 30, 'alice@example.com')
    insert_data('Bob', 25, 'bob@example.com')

    print("Before update:")
    for row in query_data():
        print(row)

    update_data('Alice', 35)

    print("After update:")
    for row in query_data():
        print(row)

    delete_data('Bob')

    print("After delete:")
    for row in query_data():
        print(row)
