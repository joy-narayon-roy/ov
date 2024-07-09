import threading
import requests


def fetch_data(url):
    response = requests.get(url)
    return response.text


def main():
    urls = [
        'https://jsonplaceholder.typicode.com/todos/1',
        'https://jsonplaceholder.typicode.com/todos/2',
        'https://jsonplaceholder.typicode.com/todos/3',
        'https://jsonplaceholder.typicode.com/todos/4',
        'https://jsonplaceholder.typicode.com/todos/5',
    ]

    threads = []
    results = []

    def fetch_data_thread(url):
        result = fetch_data(url)
        results.append(result)

    # Create and start threads for each URL
    for url in urls:
        thread = threading.Thread(target=fetch_data_thread, args=(url,))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print(results.__len__())


if __name__ == "__main__":
    main()
