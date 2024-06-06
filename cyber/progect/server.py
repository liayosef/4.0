"""
athor: lia yosef
date:31/5/2024
name: four by four
"""
import socket
import pickle
import time

import numpy as np

import protocol

ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    """
    Create a 6x7 Connect Four board initialized with zeros.

    Returns:
        np.ndarray: A 6x7 matrix filled with zeros representing the game board.
    """
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def drop_piece(board, row, col, piece):
    """
    Drop a piece into the game board at the specified row and column.

    Args:
        board (np.ndarray): The game board.
        row (int): The row index where the piece will be placed.
        col (int): The column index where the piece will be placed.
        piece (int): The piece (1 or 2) to be placed on the board.
    """
    board[row][col] = piece


def print_board(board):
    """
    Print the game board, flipping it upside down for better visualization.

    Args:
        board (np.ndarray): The game board.
    """
    print(np.flip(board, 0))


def is_valid_location(board, col):
    """
    Check if a column is a valid location to drop a piece (i.e., it is not full).

    Args:
        board (np.ndarray): The game board.
        col (int): The column index to check.

    Returns:
        bool: True if the column is a valid location, False otherwise.
    """
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    """
    Get the next open row in the specified column.

    Args:
        board (np.ndarray): The game board.
        col (int): The column index to check.

    Returns:
        int: The row index of the next open spot in the column.
    """
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def winning_move(board, piece):
    """
    Check if the specified piece has a winning move on the board.

    Args:
        board (np.ndarray): The game board.
        piece (int): The piece (1 or 2) to check for a winning move.

    Returns:
        bool: True if there is a winning move, False otherwise.
    """
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                c + 3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][
                c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][
                c + 3] == piece:
                return True


def is_board_full(board):
    """
    Check if the game board is full.

    Args:
        board (np.ndarray): The game board.

    Returns:
        bool: True if the board is full, False otherwise.
    """
    return not any(0 in row for row in board)


def server_program():
    """
    Start the Connect Four server program.
    The server waits for two clients to connect and then facilitates the game between them.
    """
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
        other_player_socket = connected_clients[1 - turn]

        # Receive column choice from active player
        col_choice = int(protocol.recv_protocol(active_player_socket).decode())

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
