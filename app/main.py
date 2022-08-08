import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    client_connection, _ = server_socket.accept() # wait for client

    while True:
        client_connection.recv(1024) # data received from client
        client_connection.send(b"+PONG\r\n") # hardcode pong with RESP


if __name__ == "__main__":
    main()
