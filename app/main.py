import socket
import threading


def handle_connection(conn):
    while True:
        try:
            command = conn.recv(1024)  # data received from client
            print(command)
            if command == "*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n":
                conn.send(b"+hey\r\n")
            else:
                conn.send(b"+PONG\r\n")  # hardcode pong with RESP
        except ConnectionError:
            break # terminate while loop if client disconnects


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        client_connection, _ = server_socket.accept()  # wait for client

        # handle concurrent clients in parallel,
        # and not block main thread by sequentially handling one connection at a time
        threading.Thread(target=handle_connection, args=(client_connection,)).start()


if __name__ == "__main__":
    main()
