from typing import List, Optional


class RESPResponseBuilder:

    @staticmethod
    def encode_simple_string(message: str) -> bytes:
        return_message = f"+{message}\r\n"
        return return_message.encode()

    @staticmethod
    def encode_bulk_strings(message: Optional[str]) -> bytes:
        if message is None:
            return b"$-1\r\n"
        return_message = f"${len(message)}\r\n{message}\r\n"
        return return_message.encode()

    @staticmethod
    def encode_arrays(messages: List[str]) -> bytes:
        return_message = ""
        if len(messages) == 1:
            print('entered')
            return RESPResponseBuilder.encode_simple_string(messages[0])

        length_identifier = f"*{len(messages)}"
        return_message += length_identifier + '\r\n'
        for message in messages:
            return_message += f"${len(message)}\r\n{message}\r\n"
        return return_message.encode()

    @staticmethod
    def encode_error(message="something unexpected happened") -> bytes:
        return_message = f"-Error {message}\r\n"
        return return_message.encode()