import socket
import threading
from typing import List, Optional


class ByteStringParser:
    COMMAND_IDENTIFIER_INDEX = 2

    def __init__(self, byte_str) -> None:
        self.byte_str = byte_str
        self.decoded_str_list = []
        self.decoded_str_list_simple = []
        self.decode()

    def decode(self) -> List[str]:
        self.decoded_str_list = self.byte_str.decode().strip('\r\n').split("\r\n")
        # print(self.byte_str, self.decoded_str_list)
        return self.decoded_str_list

    def get_command(self) -> Optional[str]:
        try:
            return self.decoded_str_list[self.COMMAND_IDENTIFIER_INDEX]
        except IndexError:
            return None

    def get_args(self) -> List[Optional[str]]:
        try:
            num_args = int(self.decoded_str_list[0][1]) - 1
            return [self.decoded_str_list[4 + index * 2] for index in range(num_args)]
        except IndexError:
            return []


class RESPResponseBuilder:
    @staticmethod
    def encode_simple_string(message: str) -> bytes:
        return_message = f"+{message}\r\n"
        return return_message.encode()

    @staticmethod
    def encode_arrays(messages: List[str]) -> bytes:
        return_message = ""
        length_identifier = f"*{len(messages)}"
        return_message += length_identifier + '\r\n'
        for message in messages:
            return_message += f"${len(message)}\r\n{message}\r\n"
        return return_message.encode()


def handle_connection(conn):
    while True:
        try:
            command_in_bytes = conn.recv(1024)  # data received from client
            parser = ByteStringParser(command_in_bytes)
            command_text = parser.get_command()

            if command_text.upper() == "ECHO":
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
