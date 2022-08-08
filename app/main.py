import socket
import threading

def decode_bytes_string(byte_string):
    pass

def handle_connection(conn):
    while True:
        try:
            command_in_bytes = conn.recv(1024)  # data received from client

            command_string_list = command_in_bytes.decode().split("\r\n")
            print(command_in_bytes, command_string_list)

            command_text = command_string_list[2]
            command_length = command_string_list[0][0]

            if command_text.upper() == "ECHO":
                return_message = f"+{command_string_list[4]}\r\n"
                conn.send(return_message.encode())
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
