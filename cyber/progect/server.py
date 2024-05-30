import socket
import pickle
import numpy as np

ROW_COUNT = 6
COLUMN_COUNT = 7

def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(5)
    print("Server started and listening for connections on port 12345...")

    connected_clients = []

    while len(connected_clients) < 2:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted new connection from {client_address}")

        message = client_socket.recv(1024).decode('utf-8')
        if message.strip() == "connectim":
            connected_clients.append(client_socket)
            print(f"Client {client_address} connected")

    print("Both clients connected. Sending game board...")

    game_board = create_board()
    game_board_pickle = pickle.dumps(game_board)

    for client_socket in connected_clients:
        client_socket.sendall(game_board_pickle)

    print("Game data sent. Waiting for client actions.")

    while True:
        for client_socket in connected_clients:
            # Handle client actions here
            pass

if __name__ == "__main__":
    server_program()









