import socket
import threading
from typing import List, Optional

from app.byte_string_parser import ByteStringParser
from app.resp_response_builder import RESPResponseBuilder


def handle_connection(conn):
    while True:
        try:
            command_in_bytes = conn.recv(1024)  # data received from client
            parser = ByteStringParser(command_in_bytes)
            command_text = parser.get_command()

            if command_text and command_text.upper() == "ECHO":
                args: List[Optional[str]] = parser.get_args()
                return_message = RESPResponseBuilder().encode_arrays(args)
                conn.send(return_message)
            else:
                conn.send(b"+PONG\r\n")  # hardcode pong with RESP
        except ConnectionError:
            break  # terminate while loop if client disconnects


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
