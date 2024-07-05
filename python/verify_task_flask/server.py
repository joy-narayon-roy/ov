import socket

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    print(f"Connection from {address} has been established!")

    while True:
        data = conn.recv(1024).decode()
        # if not data:
            # break
        print(f"Received from client: {data}")
        conn.send(data.encode())  # echo back the data to the client
    conn.close()

if __name__ == "__main__":
    server_program()
