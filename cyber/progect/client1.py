import errno
import select
import socket
import pygame
import sys
import pickle

import protocol

# Define colors
LIGHT_PINK = (255, 128, 192)
PURPLE = (128, 128, 255)
DARK_BLUE = (0, 0, 160)
DARK_PINK = (255, 0, 128)
Server_Port = 12345
SQUARESIZE = 80
RADIUS = int(SQUARESIZE / 2 - 5)
COLUMN_COUNT = 7
ROW_COUNT = 6
Width = COLUMN_COUNT * SQUARESIZE
Height = (ROW_COUNT + 1) * SQUARESIZE
Size = (Width, Height)
Screen = pygame.display.set_mode(Size)

def draw_board(screen, board, SQUARESIZE, RADIUS):
    height = (len(board) + 1) * SQUARESIZE
    for c in range(len(board[0])):
        for r in range(len(board)):
            pygame.draw.rect(screen, LIGHT_PINK, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, PURPLE, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(len(board[0])):
        for r in range(len(board)):
            if board[r][c] == 1:
                pygame.draw.circle(screen, DARK_BLUE, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, DARK_PINK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def main():
    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Enter the server IP address: ")

    try:
        print(f"Connecting to server at {server_ip}:{Server_Port}...")
        client_socket.connect((server_ip, Server_Port))
        print("Connected to the server.")

        client_socket.sendall(protocol.send_protocol(b"connectim"))
        # client_socket.setblocking(False)

        pygame.init()

        # Define screen size and other parameters
        pygame.display.set_caption("Connect Four client1")

        # Load and display the opening screen
        opening_screen = pygame.image.load('start.webp')
        opening_screen = pygame.transform.scale(opening_screen, (Width, Height))
        Screen.blit(opening_screen, (0, 0))
        pygame.display.update()


        # Wait for the player to click the mouse to start the game
        while pygame.event.wait().type != pygame.MOUSEBUTTONDOWN:
            pass

        # Main game loop
        my_turn = False
        game = True
        while game:
            # Receive game board from server
            rlist, _, _ = select.select([client_socket], [client_socket], [client_socket])
            if len(rlist) > 0:
                print("got data")
                data = protocol.recv_protocol(client_socket)
                print(data)
                if data == b'win' or data == b'lose' or data == b'draw':
                    game = False
                else:
                    my_turn = not my_turn
                    print(my_turn)
                    game_board = pickle.loads(data)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and my_turn:
                    x = event.pos[0]
                    col = int(x // SQUARESIZE)

                    client_socket.sendall(protocol.send_protocol(str(col).encode('utf-8')))

            if game_board is not None:
                draw_board(Screen, game_board, SQUARESIZE, RADIUS)

    except Exception as e:
        print(f"An error occurred: {e}")
        client_socket.close()


if __name__ == "__main__":
    main()