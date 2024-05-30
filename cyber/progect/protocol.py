"""
Author:lia yosef
Date:14.12.23
program name: 2.7
"""
import socket


def send_protocol(message):
    """
    returns a string with the lenght
    :param message: the message
    :return: the message with her lenght
    """
    length = str(len(message))
    message1 = length.zfill(10)
    message = message1 + message
    return message


def recv_protocol(socket1):
    """
    gets the socket the lenght and the message
    :param socket:the socket contaninig the full message
    :return:the messag without her lenght
    """
    length = ""
    message = ""
    try:
        while len(length) < 10:
            length += socket1.recv(1).decode()
            print(length)
        print(f"msg length: {length}")
        while len(message) < int(length):
            message += socket1.recv(int(length) - len(message)).decode()
        print(f"msg is: {message}")
    except socket.error as err:
        print("in recv: " + err)
        message = "error"
    return message
