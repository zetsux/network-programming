import sys
import unittest
from unittest.mock import patch, MagicMock
import socket
import json
from io import StringIO
import base64

def fetch_headers(username, password):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
        sck.connect(('httpbin.org', 80))
        headers = [
            "GET /headers HTTP/1.1",
            "Host: httpbin.org",
            "Authorization: Basic " + base64.b64encode(f"{username}:{password}".encode()).decode(),
            "X-Custom-Header: Test123",
            "Connection: close",
        ]
        request = "\r\n".join(headers) + "\r\n\r\n"

        sck.send(request.encode())
        response = b''
        while True:
            data = sck.recv(1024)
            if not data:
              break
            response += data

        result = response.split(b"\r\n\r\n")[-1]
        return result.decode()


# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestFetchHeaders(unittest.TestCase):
    @patch('socket.socket')
    def test_fetch_headers(self, mock_socket):
        # Setup the mocked socket instance
        mock_sock_instance = MagicMock()
        mock_socket.return_value.__enter__.return_value = mock_sock_instance

        # Define the mock response from the server
        response_body = {"success": "Received headers"}
        http_response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Length: {}\r\n"
            "\r\n"
            "{}".format(len(json.dumps(response_body)), json.dumps(response_body))
        )
        mock_sock_instance.recv.side_effect = [http_response.encode('utf-8'), b'']

        # Call the function
        body = fetch_headers('user', 'pass')

        # Assertions to check if the response body is correctly returned
        mock_sock_instance.connect.assert_called_once_with(('httpbin.org', 80))
        print(f"connect called with: {mock_sock_instance.connect.call_args}")
        
        mock_sock_instance.send.assert_called_once()
        print(f"send called with: {mock_sock_instance.send.call_args}")

        mock_sock_instance.recv.assert_called()
        print(f"recv called with: {mock_sock_instance.recv.call_args}")

        assert_equal(json.dumps(response_body), body)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        return_data = fetch_headers('user', 'pass')
        print(return_data)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)
