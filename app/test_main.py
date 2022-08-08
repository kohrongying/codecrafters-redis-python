import unittest

from app.main import ByteStringParser, RESPResponseBuilder


class TestByteStringParser(unittest.TestCase):
    def test_decode_bstring(self):
        bstr = b"*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n"
        p = ByteStringParser(bstr)
        actual = p.decoded_str_list
        self.assertEqual(actual, ['*2', '$4', 'ECHO', '$3', 'hey'])

    def test_get_command_should_return_echo(self):
        bstr = b"*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n"
        p = ByteStringParser(bstr)
        actual = p.get_command()
        self.assertEqual(actual, 'ECHO')

    def test_get_command_should_return_None(self):
        bstr = b"$0\r\n\r\n"
        p = ByteStringParser(bstr)
        actual = p.get_command()
        self.assertEqual(actual, None)

    def test_get_args(self):
        bstr = b"*3\r\n$4\r\nECHO\r\n$3\r\nhey\r\n$5\r\nworld\r\n"
        p = ByteStringParser(bstr)
        actual = p.get_args()
        self.assertEqual(actual, ['hey', 'world'])


class TestRESPResponseBuilder(unittest.TestCase):
    def test_encode_simple_string(self):
        echo_text = "hello"
        self.assertEqual(RESPResponseBuilder().encode_simple_string(echo_text), b"+hello\r\n")

    def test_encode_bulk_string(self):
        messages = ["hello", "world"]
        self.assertEqual(RESPResponseBuilder().encode_arrays(messages),
                         b"*2\r\n$5\r\nhello\r\n$5\r\nworld\r\n")

    def test_encode_bulk_string_single_arg(self):
        messages = ["hello"]
        self.assertEqual(RESPResponseBuilder().encode_arrays(messages),
                         b"+hello\r\n")


if __name__ == "__main__":
    print('hi')
