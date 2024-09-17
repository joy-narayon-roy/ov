from concurrent.futures import ThreadPoolExecutor
from main import worker


def task(n):
    worker(n)


def main():
    try:
        total = 4
        with ThreadPoolExecutor(max_workers=total) as executor:
            for i in range(total):
                executor.submit(task, i)
    except KeyboardInterrupt:
        print("Caught Ctrl+C, shutting down gracefully...")


if __name__ == "__main__":
    main()
