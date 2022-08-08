import socket
import threading
from typing import List, Optional

from app.byte_string_parser import ByteStringParser
from app.resp_response_builder import RESPResponseBuilder

redis_store = {}


def handle_connection(conn):
    while True:
        try:
            command_in_bytes = conn.recv(1024)  # data received from client
            parser = ByteStringParser(command_in_bytes)
            command_text = parser.get_command()
            args: List[Optional[str]] = parser.get_args()

            if command_text and command_text.upper() == "ECHO":
                return_message = RESPResponseBuilder().encode_arrays(args)
                conn.send(return_message)
            elif command_text and command_text.upper() == "GET":
                if len(args) != 1:
                    raise Exception("Can only GET one argument")
                try:
                    stored_value = redis_store[args]
                    message = RESPResponseBuilder().encode_bulk_strings(stored_value)
                    conn.send(message)
                except KeyError:
                    message = RESPResponseBuilder().encode_bulk_strings("(nil)")
                    conn.send(message)
            elif command_text and command_text.upper() == "SET":
                if len(args) != 2:
                    raise Exception("Can only SET key value")
                try:
                    key = args[0]
                    value = args[1]
                    redis_store[key] = value
                    message = RESPResponseBuilder().encode_bulk_strings("OK")
                    conn.send(message)
                except:
                    message = RESPResponseBuilder().encode_bulk_strings("help")
                    conn.send(message)

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
