"""
 HTTP Server Shell
 Author: Barak Gonen and Nir Dweck
 Purpose: Provide a basis for Ex. 4
 Note: The code is written in a simple way, without classes, log files or
 other utilities, for educational purpose
 Usage: Fill the missing functions and constants
"""
import socket
import os

# TO DO: set constants

QUEUE_SIZE = 10
IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 2
DEFAULT_URL = r"C:\webroot\index.html"
WEB_ROOT = r"C:\webroot"
REDIRECTION_DICTIONARY = {
    302: "302 MOVED TEMPORARILY", 400: "400 BAD REQUEST", 403: "403 FORBIDDEN",
    404: "404 NOT FOUND", 500: "500 INTERNAL SERVER ERROR"
}


def get_file_data(file_name):
    """
    Get data from file
    :param file_name: the name of the file
    :return: the file data in a string
    """
    try:
        with open(WEB_ROOT + "\\" + file_name, 'r') as file:
            file_data = file.read()
            return file_data
    except FileNotFoundError:
        return f"File '{file_name}' not found."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def handle_client_request(resource, client_socket):
    """
    Check the required resource, generate proper HTTP response and send
    to client
    :param resource: the required resource
    :param client_socket: a socket for the communication with the client
    :return: None
    """

    if resource == "/":
        uri = DEFAULT_URL
    else:
        uri = resource

    # Check for redirections (unchanged)
    if uri in REDIRECTION_DICTIONARY:
        target_url = REDIRECTION_DICTIONARY[uri]
        http_header = f"HTTP/1.1 302 Found\r\nLocation: {target_url}\r\n\r\n"
        client_socket.send(http_header.encode())
        return

    # Determine content type and handle file retrieval (optimized)
    file_extension = os.path.splitext(uri)[1].lower()
    content_type = {
        '.html': "text/html;charset=utf-8",
        '.jpg': "image/jpeg",
        '.css': "text/css",
        '.js': "text/javascript; charset=UTF-8",
        '.txt': "text/plain",
        '.ico': "image/x-icon",
        '.gif': "image/gif",
        '.png': "image/png",
    }.get(file_extension)

    try:
        if content_type.startswith("text/"):
            with open(uri, 'r') as f:
                data = f.read().encode()
        else:  # Assume binary content
            with open(uri, 'rb') as f:
                data = f.read()

        http_header = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {len(data)}\r\n\r\n"
    except FileNotFoundError:
        http_header = f"HTTP/1.1 404 Not Found\r\n\r\n"
        data = b''
    except Exception as e:
        http_header = f"HTTP/1.1 500 Internal Server Error\r\n\r\n"
        data = b''

    # Send response
    http_response = http_header.encode() + data
    client_socket.send(http_response)


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns the URI if valid,
    otherwise returns an empty string.

    :param request: the request which was received from the client
    :return: the URI of the requested resource if valid, otherwise an empty string
    """

    lines = request[0].split(' ')
    if len(lines) != 3 or lines[2] != "HTTP/1.1" or lines[0] != "GET":
        return False, " "
    else:
        return True, lines[1]


def handle_client(client_socket):
    """
    Handles client requests: verifies client's requests are legal HTTP, calls
    function to handle the requests
    :param client_socket: the socket for the communication with the client
    :return: None
    """

    print('Client connected')

    try:
        while True:
            # Receive client request in chunks and combine them
            client_request = b''  # Empty byte string to store the request
            while True:
                chunk = client_socket.recv(1024)  # Receive 1024 bytes at a time
                if not chunk:  # Empty chunk means client closed connection
                    break
                client_request += chunk  # Append chunk to request

                # Check if request is complete (ends with double newline)
                if b'\r\n\r\n' in client_request:
                    break

            # Validate the HTTP request
            valid_http, resource = validate_http_request(client_request.decode())
            print(resource)
            if valid_http:
                print('Got a valid HTTP request')
                handle_client_request(resource, client_socket)
            else:
                print('Error: Not a valid HTTP request')
                break

    except (ConnectionError, socket.timeout) as e:  # Handle more specific errors
        print(f'Client disconnected: {e}')
    finally:
        client_socket.close()
        print('Closing connection')


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        print("Listening for connections on port %d" % PORT)

        while True:
            client_socket, client_address = server_socket.accept()
            try:
                print('New connection received')
                client_socket.settimeout(SOCKET_TIMEOUT)
                handle_client(client_socket)
            except socket.error as err:
                print('received socket exception - ' + str(err))
            finally:
                client_socket.close()
    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == "__main__":
    # Call the main handler function
    main()
