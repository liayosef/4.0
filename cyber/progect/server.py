import socket
import pickle
import time

import numpy as np

import protocol

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def print_board(board):
    print(np.flip(board, 0))


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def is_board_full(board):
    return not any(0 in row for row in board)


def server_program():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))
    server_socket.listen(2)
    print("Server started and listening for connections on port 12345...")

    connected_clients = []

    while len(connected_clients) < 2:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted new connection from {client_address}")

        message = protocol.recv_protocol(client_socket).decode()
        if message.strip() == "connectim":
            connected_clients.append(client_socket)
            print(f"Client {client_address} connected")

    print("Both clients connected. Sending game board...")

    game_board = create_board()
    game_board_pickle = pickle.dumps(game_board)

    turn = 0  # Initialize turn variable
    current_player = 1  # Initialize current player (1 or 2)

    for client_socket in connected_clients:
        client_socket.sendall(protocol.send_protocol(game_board_pickle))

    print("Game data sent. Waiting for client actions.")

    while True:
        active_player_socket = connected_clients[turn]
        # active_player_socket.sendall(b"YOUR TURN")
        # print("sent turn to active player")
        other_player_socket = connected_clients[1 - turn]

        # Receive column choice from active player
        col_choice = int(protocol.recv_protocol(active_player_socket).decode())
        # print("col " + col_choice)


        # Update game board
        row = get_next_open_row(game_board, col_choice)
        drop_piece(game_board, row, col_choice, current_player)

        # Check for win or draw
        if winning_move(game_board, current_player):
            # Send updated game board to both clients
            game_board_pickle = pickle.dumps(game_board)
            for client_socket in connected_clients:
                client_socket.sendall(protocol.send_protocol(game_board_pickle))

            # Send win message to winner
            active_player_socket.sendall(protocol.send_protocol(b"win"))
            other_player_socket.sendall(protocol.send_protocol(b"lose"))
            print(f"Player {current_player} wins!")
            break
        elif is_board_full(game_board):
            # Send updated game board to both clients
            game_board_pickle = pickle.dumps(game_board)
            for client_socket in connected_clients:
                client_socket.sendall(protocol.send_protocol(game_board_pickle))

            # Send draw message to both players
            active_player_socket.sendall(protocol.send_protocol(b"draw"))
            other_player_socket.sendall(protocol.send_protocol(b"draw"))
            print("It's a draw!")
            break
        else:
            # Send updated game board to both clients
            game_board_pickle = pickle.dumps(game_board)
            for client_socket in connected_clients:
                client_socket.sendall(protocol.send_protocol(game_board_pickle))

            # Switch turns
            turn = 1 - turn
            current_player = 1 if current_player == 2 else 2

    server_socket.close()


if __name__ == "__main__":
    server_program()