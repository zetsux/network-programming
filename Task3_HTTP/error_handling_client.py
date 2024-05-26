import unittest
from unittest import mock
from io import StringIO
import http.client
import sys

def check_url():
    conn = http.client.HTTPSConnection("jsonplaceholder.typicode.com")
    
    # Send a GET request to an invalid URL to test response handling
    conn.request("GET", "/invalidurl")
    
    # Get the response from the server
    response = conn.getresponse()
    
    # Close the connection
    conn.close()
    
    # Check the response status
    if response.status != 200:
        return "Request Failed"
    else:
        return "Request Succeeded"
        

# A 'null' stream that discards anything written to it
class NullWriter(StringIO):
    def write(self, txt):
        pass


def assert_equal(parameter1, parameter2):
    if parameter1 == parameter2:
        print(f'test attribute passed: {parameter1} is equal to {parameter2}')
    else:
        print(f'test attribute failed: {parameter1} is not equal to {parameter2}')


class TestCheckUrl(unittest.TestCase):
    @mock.patch('http.client.HTTPSConnection')
    def test_check_url_request_failed(self, mock_conn):
        mock_response = mock.Mock()
        mock_response.status = 404
        mock_conn.return_value.getresponse.return_value = mock_response

        result = check_url()

        mock_conn.assert_called_once_with("jsonplaceholder.typicode.com")
        print(f"connection called with: {mock_conn.call_args}")

        mock_conn.return_value.request.assert_called_once_with("GET", "/invalidurl")
        print(f"request called with: {mock_conn.return_value.request.call_args}")

        mock_conn.return_value.close.assert_called_once()
        print(f"connection closed: {mock_conn.return_value.close.call_args}")

        assert_equal(result, "Request Failed")

    @mock.patch('http.client.HTTPSConnection')
    def test_check_url_request_succeeded(self, mock_conn):
        mock_response = mock.Mock()
        mock_response.status = 200
        mock_conn.return_value.getresponse.return_value = mock_response

        result = check_url()

        mock_conn.assert_called_once_with("jsonplaceholder.typicode.com")
        print(f"connection called with: {mock_conn.call_args}")

        mock_conn.return_value.request.assert_called_once_with("GET", "/invalidurl")
        print(f"request called with: {mock_conn.return_value.request.call_args}")

        mock_conn.return_value.close.assert_called_once()
        print(f"connection closed: {mock_conn.return_value.close.call_args}")

        assert_equal(result, "Request Succeeded")

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'run':
        status = check_url()
        print(status)

    # run unit test to test locally
    # or for domjudge
    runner = unittest.TextTestRunner(stream=NullWriter())
    unittest.main(testRunner=runner, exit=False)