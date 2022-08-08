import unittest


class Test(unittest.TestCase):
    def test_decode_bstring(self):
        bstr = b"*2\r\n$4\r\nECHO\r\n$3\r\nhey\r\n"
        self.assertEqual(bstr.decode().split('\r\n'), ['*2', '$4', 'ECHO', '$3', 'hey', ''])

    def test_format_bstring(self):
        echo_text = "hello"
        bstr = f"+{echo_text}\r\n"
        self.assertEqual(bstr.encode(), b"+hello\r\n")


if __name__ == "__main__":
    print('hi')
