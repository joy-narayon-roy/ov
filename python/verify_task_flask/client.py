import socket


def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    message = "Hello, Server!"
    client_socket.send(message.encode())
    data = client_socket.recv(1024).decode()
    print(f"Received from server: {data}")

    client_socket.close()


if __name__ == "__main__":
    client_program()
