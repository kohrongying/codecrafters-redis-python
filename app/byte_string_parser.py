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