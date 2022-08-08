import socket
import threading


def ping_function(conn):
    conn.recv(1024)  # data received from client
    conn.send(b"+PONG\r\n")  # hardcode pong with RESP


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    client_connection, _ = server_socket.accept()  # wait for client

    while True:
        x = threading.Thread(target=ping_function, args=(client_connection,))
        x.start()


if __name__ == "__main__":
    main()
