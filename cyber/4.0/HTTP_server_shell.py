"""
 HTTP Server Shell
 Author: lia yosef
 Purpose:  Ex. 4
"""
import logging
import socket
import os

# TO DO: set constants
UPLOAD = r"C:/users/user/Onedrive/Desktop/cyber/4.0/UPLOAD"
QUEUE_SIZE = 10
IP = '127.0.0.1'
PORT = 80
SOCKET_TIMEOUT = 2
MAX_PACKET = 1024
DEFAULT_URL = r"/index.html"
WEB_ROOT = r"C:/users/user/Onedrive/Desktop/cyber/4.0/webroot"
REDIRECT_LOC = "/"
HTTP_VERSION = "HTTP/1.1"
REDIRECTION_DICTIONARY = {
    "/moved": f"302 MOVED TEMPORARILY\r\nlocation: {REDIRECT_LOC}\r\n", "/forbidden": "403 FORBIDDEN\r\n",
    "/error": "500 INTERNAL SERVER ERROR\r\n"
}

NOT_FOUND = "404 NOT FOUND\r\n"
OK_RESPONSE = "200 OKAY\r\n"
BAD_REQUEST = "400 BAD REQUEST\r\n"

CONTENT_TYPES = {
    '.html': "text/html;charset=utf-8",
    '.jpg': "image/jpeg",
    '.css': "text/css",
    '.js': "text/javascript; charset=UTF-8",
    '.txt': "text/plain",
    '.ico': "image/x-icon",
    '.gif': "image/gif",
    '.png': "image/png",
}


def upload(file_bytes, file_name):
    """
    The function gets a file's data and name and saves it to the upload folder.
    :param file_bytes: the file's bytes.
    :param file_name: the name of the file
    :return: a 200OK response if the upload succeeded and a 400 BAD REQUEST otherwise.
    """
    try:
        file_path = UPLOAD + '//' + file_name
        with open(file_path, "wb") as binary_file:
            binary_file.write(file_bytes)
        return_value = OK_RESPONSE
    except Exception as e:
        logging.error("received socket exception: " + str(e))
        return_value = BAD_REQUEST

    return return_value


def calculate_next(request):
    query_params = request.split('?')[1] if '?' in request else ""
    param_list = query_params.split('&')
    num_parameter = next((param for param in param_list if param.startswith('num=')), None)
    if num_parameter:
        num_value = num_parameter.split('num=')[1]
        try:
            num_value = int(num_value)
            print(num_value)
            return str(num_value + 1)
        except ValueError:
            return BAD_REQUEST


def calculate_area(file_name):
    start_index_height = file_name.find('height=') + len('height=')
    end_index_height = file_name.find('&', start_index_height) if '&' in file_name else len(file_name)
    num_value_height = file_name[start_index_height:end_index_height]
    start_index_width = file_name.find('width=') + len('width=')
    end_index_width = file_name.find('&', start_index_width) if '&' in file_name else len(file_name)
    num_value_width = file_name[start_index_width:end_index_width]
    area = (num_value_width * num_value_height)/2
    if (num_value_width == " " or num_value_height == " " or not num_value_height.isnumeric()
            or not num_value_width.isnumeric()):
        return BAD_REQUEST
    else:
        return str(area)


def get_file_data(file_name):
    """
    Get data from file
    :param file_name: the name of the file
    :return: the file data in a string
    """
    r_data = b''
    try:
        with open(file_name, 'rb') as file:
            file_data = file.read()
            r_data = file_data
    except FileNotFoundError:
        logging.error(f"File '{file_name}' not found.")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}".encode())
    finally:
        return r_data


def handle_client_request(resource, client_socket):
    """
    Check the required resource, generate proper HTTP response and send
    to client
    :param resource: the required resource
    :param client_socket: a socket for the communication with the client
    :return: None
    """
    res = ""
    data = b''
    if resource == "/":
        uri = DEFAULT_URL
    else:
        uri = resource
    # Check for redirections (unchanged)
    if uri in REDIRECTION_DICTIONARY:
        res = HTTP_VERSION + " " + REDIRECTION_DICTIONARY[uri] + "\r\n"
    else:

        # Determine content type and handle file retrieval (optimized)

        data = get_file_data(WEB_ROOT + uri)

        if data != b'':
            file_extension = os.path.splitext(uri)[1].lower()
            content_type = CONTENT_TYPES[file_extension]
            res = HTTP_VERSION + " " + OK_RESPONSE
            res += "Content-Type: " + content_type + "\r\n"
            res += "Content-Length: " + str(len(data)) + "\r\n\r\n"
            print(res)
        else:
            res = HTTP_VERSION + " " + NOT_FOUND + "\r\n"

    return res.encode() + data


def send(sock, msg):
    sent = 0
    try:
        while sent < len(msg):
            sent += sock.send(msg[sent:])
    except socket.error as err:
        logging.error(f"somthing went wrong while sending data: {err}")


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns the URI if valid,
    otherwise returns the error 400 bad request

    :param request: the request which was received from the client
    :return: the URI of the requested resource if valid, otherwise an empty string
    """
    print(request)
    request = request.split('\r\n')
    lines = request[0].split(' ')
    print(lines)
    if len(lines) != 3 or lines[2] != "HTTP/1.1" or lines[0] != "GET" or not lines[1].startswith("/"):
        return False, ""
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
                chunk = client_socket.recv(MAX_PACKET)
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
                res = handle_client_request(resource, client_socket)
                send(client_socket, res)
            else:
                print('Error: Not a valid HTTP request')
                send(client_socket, (HTTP_VERSION + " " + BAD_REQUEST + "\r\n\r\n").encode())
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
