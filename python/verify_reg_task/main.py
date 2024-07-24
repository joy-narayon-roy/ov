import sqlite3
from context import data_contest

def worker():
    print(data_contest)

def main():
    worker()

if __name__ == "__main__":
    main()