import socket
import threading
from typing import List, Optional

from app.redis_store import RedisStore
from app.resp_decoder import RESPDecoder
from app.resp_response_builder import RESPResponseBuilder

redis_store = RedisStore()


def handle_connection(conn):
    while True:
        try:
            command_in_bytes = conn.recv(1024)  # data received from client
            parser = RESPDecoder(command_in_bytes)
            command_text = parser.get_command()
            args: List[Optional[str]] = parser.get_args()
            print('args', args)

            if command_text and command_text.upper() == "ECHO":
                handle_echo(args, conn)
            elif command_text and command_text.upper() == "GET":
                handle_get(args, conn)
            elif command_text and command_text.upper() == "SET":
                handle_set(args, conn)
            else:
                message = RESPResponseBuilder().encode_simple_string("PONG")
                conn.send(message)  # hardcode pong with RESP
        except ConnectionError:
            break  # terminate while loop if client disconnects


def handle_set(args, conn):
    if len(args) != 2:
        message = RESPResponseBuilder().encode_error("only accept 2 arguments")
    else:
        key = args[0]
        value = args[1]
        response = redis_store.set(key, value)
        if response == "OK":
            message = RESPResponseBuilder().encode_simple_string("OK")
        else:
            message = RESPResponseBuilder().encode_bulk_strings(response)
    conn.send(message)


def handle_get(args, conn):
    if len(args) != 1:
        message = RESPResponseBuilder().encode_error("only accept 1 argument")
    else:
        key = args[0]
        stored_value = redis_store.get(key)
        if stored_value is None:
            message = RESPResponseBuilder().encode_bulk_strings("(nil)")
        elif type(stored_value) == str:
            message = RESPResponseBuilder().encode_bulk_strings(stored_value)
        else:
            message = RESPResponseBuilder().encode_error("value is not string")
    conn.send(message)


def handle_echo(args, conn):
    return_message = RESPResponseBuilder().encode_arrays(args)
    conn.send(return_message)


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
