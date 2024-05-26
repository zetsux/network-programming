import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
import socket
import json


def fetch_post_title():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
        host = "jsonplaceholder.typicode.com"
        sck.connect((host, 80))

        parts = ["GET /posts/1 HTTP/1.1", f"Host: {host}", "Connection: close"]
        request = "\r\n".join(parts) + "\r\n\r\n"
        sck.send(request.encode())

        response = sck.recv(4096)
        sck.close()

        body = json.loads(response.decode().split("\r\n\r\n")[1])
        return body["title"]
        # title = response.split("\r\n\r\n")[1].split("\r\n")[0].split(": ")[1]
        # print(title)
        # return title


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f"test attribute passed: {parameter1} is equal to {parameter2}")
    else:
        print(f"test attribute failed: {parameter1} is not equal to {parameter2}")


class TestHttpRequest(unittest.TestCase):
    @patch("socket.socket")
    def test_fetch_post_title(self, mock_socket):
        # Setup mock
        sample_response = 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"}'
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance
        mock_sock_instance.recv.return_value = sample_response.encode()

        # Call function
        title = fetch_post_title()

        # Assertions
        mock_socket.assert_called_once()
        mock_sock_instance.connect.assert_called_with(
            ("jsonplaceholder.typicode.com", 80)
        )
        print(f"connect called with: {mock_sock_instance.connect.call_args}")

        mock_sock_instance.send.assert_called_once()
        print(f"send called with: {mock_sock_instance.send.call_args}")

        mock_sock_instance.recv.assert_called_once()
        print(f"recv called with: {mock_sock_instance.recv.call_args}")

        assert_equal(
            title,
            "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        )


if __name__ == "__main__":
    # to run the script without unit test:
    # python solution.py run
    if len(sys.argv) == 2 and sys.argv[1] == "run":
        title = fetch_post_title()
        print(title)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
